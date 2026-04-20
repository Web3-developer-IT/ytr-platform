from django.db import models
from django.contrib.auth.models import User
from core.models import Listing


class Message(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    content = models.TextField(blank=True)

    attachment = models.FileField(
        upload_to="messaging/attachments/",
        blank=True,
        null=True,
        help_text="Optional image or short video shared in the thread.",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    read = models.BooleanField(default=False)

    def preview_snippet(self, max_len: int = 52) -> str:
        t = (self.content or "").strip()
        if t:
            return (t[:max_len] + "…") if len(t) > max_len else t
        if self.attachment:
            name = self.attachment.name.lower()
            if any(name.endswith(x) for x in (".mp4", ".webm", ".mov")):
                return "[Video attached]"
            return "[Photo attached]"
        return "…"

    def attachment_media_kind(self) -> str | None:
        if not self.attachment:
            return None
        n = (self.attachment.name or "").lower()
        if any(n.endswith(x) for x in (".mp4", ".webm", ".mov")):
            return "video"
        return "image"

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
