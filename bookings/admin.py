from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "start_date", "end_date", "approved", "created_at")
    list_filter = ("approved", "start_date", "end_date")
    search_fields = ("listing__title", "user__username")
    actions = ["approve_bookings"]

    def approve_bookings(self, request, queryset):
        queryset.update(approved=True)
    approve_bookings.short_description = "Approve selected bookings"