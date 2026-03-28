from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils import timezone

from .models import PlatformNotification, UserDocument, UserNotificationRead, UserProfile

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "updated_at")
    search_fields = ("user__username", "user__email", "phone")
    raw_id_fields = ("user",)


@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "document_type",
        "status",
        "file_link",
        "submitted_at",
        "reviewed_at",
        "reviewed_by",
    )
    list_filter = ("status", "document_type", "submitted_at")
    search_fields = ("user__username", "user__email", "review_notes")
    readonly_fields = ("submitted_at", "reviewed_at", "file_link")
    raw_id_fields = ("user", "reviewed_by")
    actions = ("approve_documents", "reject_documents")
    fieldsets = (
        (None, {"fields": ("user", "document_type", "document_file", "file_link", "status")}),
        ("Review", {"fields": ("review_notes", "reviewed_by", "reviewed_at", "submitted_at")}),
    )

    @admin.display(description="File")
    def file_link(self, obj):
        if obj.document_file:
            url = obj.document_file.url
            return format_html('<a href="{}" target="_blank" rel="noopener">Open upload</a>', url)
        return "—"

    @admin.action(description="Approve selected documents")
    def approve_documents(self, request, queryset):
        user_ids = list(queryset.values_list("user_id", flat=True).distinct())
        updated = queryset.update(
            status=UserDocument.STATUS_APPROVED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )
        self.message_user(request, f"{updated} document(s) approved.")
        for uid in user_ids:
            PlatformNotification.objects.create(
                recipient_id=uid,
                title="Verification documents approved",
                message="Your verification documents have been approved. You can continue using booking features that require verification.",
                created_by=request.user,
                is_active=True,
            )

    @admin.action(description="Reject selected documents")
    def reject_documents(self, request, queryset):
        user_ids = list(queryset.values_list("user_id", flat=True).distinct())
        updated = queryset.update(
            status=UserDocument.STATUS_REJECTED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )
        self.message_user(request, f"{updated} document(s) rejected.")
        for uid in user_ids:
            PlatformNotification.objects.create(
                recipient_id=uid,
                title="Verification documents need attention",
                message="Your verification documents require updates. Please review admin notes and resubmit from your Documents page.",
                created_by=request.user,
                is_active=True,
            )


@admin.register(PlatformNotification)
class PlatformNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "recipient", "is_active", "created_by", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "message", "recipient__username", "recipient__email")
    readonly_fields = ("created_at",)
    raw_id_fields = ("recipient", "created_by")
    fieldsets = (
        (
            None,
            {
                "fields": ("title", "message", "recipient", "is_active"),
                "description": "Leave recipient empty to broadcast to all users (shown in-app; not email).",
            },
        ),
        ("Meta", {"fields": ("created_by", "created_at")}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(UserNotificationRead)
class UserNotificationReadAdmin(admin.ModelAdmin):
    list_display = ("user", "notification", "read_at")
    search_fields = ("user__username", "notification__title")
    list_filter = ("read_at",)
    raw_id_fields = ("user", "notification")
