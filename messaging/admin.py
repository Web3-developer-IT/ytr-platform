from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "listing", "read", "has_attachment", "created_at")

    @admin.display(boolean=True)
    def has_attachment(self, obj):
        return bool(obj.attachment)
    list_filter = ("read", "created_at")
    search_fields = ("sender__username", "receiver__username", "listing__title", "content")
