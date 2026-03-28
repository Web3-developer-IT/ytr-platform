from django.contrib import admin
from .models import Listing, ListingImage

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "category",
        "body_style",
        "verification_status",
        "location",
        "price_per_day",
        "available",
        "created_at",
    )
    list_filter = ("available", "verification_status", "category", "body_style", "created_at")
    search_fields = ("title", "owner__username", "location")
    actions = ["mark_available", "mark_unavailable"]

    def mark_available(self, request, queryset):
        queryset.update(available=True)
    mark_available.short_description = "Mark selected listings as available"

    def mark_unavailable(self, request, queryset):
        queryset.update(available=False)
    mark_unavailable.short_description = "Mark selected listings as unavailable"


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "uploaded_at")
    search_fields = ("listing__title",)