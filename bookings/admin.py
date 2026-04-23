from django.contrib import admin
from .models import Booking, HostPayout


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "listing",
        "user",
        "start_date",
        "end_date",
        "approved",
        "payment_state",
        "amount_due_total",
        "created_at",
    )
    list_filter = ("approved", "payment_state", "start_date", "end_date")
    search_fields = ("listing__title", "user__username")
    actions = ["approve_bookings"]

    def approve_bookings(self, request, queryset):
        queryset.update(approved=True)

    approve_bookings.short_description = "Approve selected bookings"


@admin.register(HostPayout)
class HostPayoutAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "owner", "amount", "commission_amount", "status", "created_at", "completed_at")
    list_filter = ("status",)
    search_fields = ("booking__listing__title", "owner__username")