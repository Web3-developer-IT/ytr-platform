from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(upload_to="profile_avatars/", blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True)
    bio = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


class UserDocument(models.Model):
    DOC_ID = "id_document"
    DOC_LICENSE = "drivers_license"
    DOC_PROOF_ADDRESS = "proof_of_address"
    DOC_OTHER = "other"
    DOC_TYPE_CHOICES = (
        (DOC_ID, "ID Document"),
        (DOC_LICENSE, "Driver's License"),
        (DOC_PROOF_ADDRESS, "Proof of Address"),
        (DOC_OTHER, "Other"),
    )

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="verification_documents",
    )
    document_type = models.CharField(max_length=32, choices=DOC_TYPE_CHOICES)
    document_file = models.FileField(upload_to="verification_documents/")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_documents",
    )
    review_notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-submitted_at",)

    def __str__(self):
        return f"{self.user.username} - {self.get_document_type_display()} ({self.status})"


class PlatformNotification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="platform_notifications",
        help_text="Leave empty for a broadcast message to all users.",
    )
    title = models.CharField(max_length=180)
    message = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_platform_notifications",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        scope = self.recipient.username if self.recipient else "Broadcast"
        return f"{self.title} [{scope}]"


class UserNotificationRead(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_reads",
    )
    notification = models.ForeignKey(
        PlatformNotification,
        on_delete=models.CASCADE,
        related_name="read_by_users",
    )
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "notification")
        ordering = ("-read_at",)

    def __str__(self):
        return f"{self.user.username} read {self.notification_id}"


REQUIRED_VERIFICATION_DOCUMENT_TYPES = {
    UserDocument.DOC_ID,
    UserDocument.DOC_LICENSE,
    UserDocument.DOC_PROOF_ADDRESS,
}


def is_user_verified(user):
    """
    A user is considered verified once *all* required document types have been approved.
    Admin staff is always treated as verified.
    """
    if not user or not getattr(user, "is_authenticated", False):
        return False
    if getattr(user, "is_staff", False):
        return True
    approved_types = set(
        UserDocument.objects.filter(user=user, status=UserDocument.STATUS_APPROVED)
        .values_list("document_type", flat=True)
    )
    return REQUIRED_VERIFICATION_DOCUMENT_TYPES.issubset(approved_types)
