from django import template
from django.conf import settings
from django.contrib.auth.models import User

from core.models import Listing
from bookings.models import Booking
from users.models import UserDocument

register = template.Library()


@register.inclusion_tag("admin/partials/ytr_admin_stats.html")
def ytr_admin_dashboard_stats():
    pending_docs = UserDocument.objects.filter(status=UserDocument.STATUS_PENDING).count()
    pending_docs_qs = (
        UserDocument.objects.filter(status=UserDocument.STATUS_PENDING)
        .select_related("user")
        .order_by("-submitted_at")[:6]
    )
    pending_bookings_qs = (
        Booking.objects.filter(approved=False)
        .select_related("listing", "user")
        .order_by("-created_at")[:6]
    )
    recent_listings_qs = (
        Listing.objects.select_related("owner")
        .order_by("-created_at")[:6]
    )
    commercial_listings = Listing.objects.filter(
        body_style__in=("Commercial", "Van", "Truck", "Bakkie", "Fleet"),
        verification_status=Listing.VERIFICATION_APPROVED,
    ).count()
    total_listings = Listing.objects.count()
    available_listings = Listing.objects.filter(available=True).count()
    availability_rate = int((available_listings * 100 / total_listings)) if total_listings else 0
    default_storage_backend = (
        (getattr(settings, "STORAGES", {}) or {}).get("default", {}).get("BACKEND", "")
    )
    static_storage_backend = (
        (getattr(settings, "STORAGES", {}) or {}).get("staticfiles", {}).get("BACKEND", "")
    )
    return {
        "total_listings": total_listings,
        "available_listings": available_listings,
        "commercial_listings": commercial_listings,
        "total_users": User.objects.filter(is_active=True).count(),
        "total_bookings": Booking.objects.count(),
        "pending_documents": pending_docs,
        "availability_rate": availability_rate,
        "pending_docs_qs": pending_docs_qs,
        "pending_bookings_qs": pending_bookings_qs,
        "recent_listings_qs": recent_listings_qs,
        "debug_mode": bool(getattr(settings, "DEBUG", False)),
        "cloudinary_enabled": "cloudinary_storage" in default_storage_backend,
        "whitenoise_enabled": "whitenoise" in static_storage_backend,
    }
