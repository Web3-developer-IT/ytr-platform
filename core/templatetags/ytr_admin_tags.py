from django import template
from django.contrib.auth.models import User

from core.models import Listing
from bookings.models import Booking
from users.models import UserDocument

register = template.Library()


@register.inclusion_tag("admin/partials/ytr_admin_stats.html")
def ytr_admin_dashboard_stats():
    pending_docs = UserDocument.objects.filter(status=UserDocument.STATUS_PENDING).count()
    commercial_listings = Listing.objects.filter(
        body_style__in=("Commercial", "Van", "Truck", "Bakkie", "Fleet"),
        verification_status=Listing.VERIFICATION_APPROVED,
    ).count()
    return {
        "total_listings": Listing.objects.count(),
        "available_listings": Listing.objects.filter(available=True).count(),
        "commercial_listings": commercial_listings,
        "total_users": User.objects.filter(is_active=True).count(),
        "total_bookings": Booking.objects.count(),
        "pending_documents": pending_docs,
    }
