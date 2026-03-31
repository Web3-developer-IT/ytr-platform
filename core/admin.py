from django.contrib import admin
from django.utils.html import format_html
from .models import Listing, ListingImage

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "thumb",
        "title",
        "owner",
        "category",
        "body_style",
        "status_chip",
        "verification_status",
        "location",
        "price_per_day",
        "available",
        "created_at",
    )
    list_filter = ("available", "verification_status", "category", "body_style", "created_at")
    search_fields = ("title", "owner__username", "location")
    list_select_related = ("owner",)
    actions = ["mark_available", "mark_unavailable"]

    def mark_available(self, request, queryset):
        queryset.update(available=True)
    mark_available.short_description = "Mark selected listings as available"

    def mark_unavailable(self, request, queryset):
        queryset.update(available=False)
    mark_unavailable.short_description = "Mark selected listings as unavailable"

    @admin.display(description="Photo")
    def thumb(self, obj):
        url = obj.primary_image_url
        if not url:
            return "—"
        return format_html(
            '<img src="{}" alt="{}" style="width:54px;height:38px;object-fit:cover;border-radius:8px;border:1px solid rgba(255,255,255,.15)">',
            url,
            obj.title,
        )

    @admin.display(description="State")
    def status_chip(self, obj):
        if not obj.available:
            bg = "rgba(180,180,180,.2)"
            color = "#ddd"
            text = "Unavailable"
        elif obj.verification_status == obj.VERIFICATION_APPROVED:
            bg = "rgba(76, 175, 80, .2)"
            color = "#a5f0a8"
            text = "Live"
        elif obj.verification_status == obj.VERIFICATION_PENDING:
            bg = "rgba(255, 193, 7, .2)"
            color = "#ffd780"
            text = "Pending review"
        else:
            bg = "rgba(244, 67, 54, .2)"
            color = "#ff9f97"
            text = "Rejected"
        return format_html(
            '<span style="display:inline-block;padding:3px 8px;border-radius:999px;background:{};color:{};font-size:11px;font-weight:700;">{}</span>',
            bg,
            color,
            text,
        )


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "uploaded_at")
    search_fields = ("listing__title",)