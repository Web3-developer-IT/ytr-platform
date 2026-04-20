"""Read-only JSON API for monitoring, dashboards, and integrations."""

from __future__ import annotations

import django
from django.conf import settings
from django.db.models import Count
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bookings.models import Booking
from core.models import Listing


class HealthView(APIView):
    """Liveness probe for Hostinger, Render, or uptime monitors."""

    permission_classes = [AllowAny]
    authentication_classes: list = []

    def get(self, request):
        return Response(
            {
                "status": "ok",
                "service": "yours-to-rent",
                "version": getattr(settings, "YTR_PLATFORM_VERSION", "1.0.0"),
                "django": django.get_version(),
                "time": timezone.now().isoformat(),
                "debug": settings.DEBUG,
                "static_url": settings.STATIC_URL,
                "cdn_static_base": getattr(settings, "YTR_STATIC_CDN_BASE", "") or None,
            }
        )


class PlatformStatsView(APIView):
    """Public aggregate counts for marketing widgets / external dashboards."""

    permission_classes = [AllowAny]
    authentication_classes: list = []

    def get(self, request):
        approved = Listing.objects.filter(
            verification_status=Listing.VERIFICATION_APPROVED
        ).count()
        pending = Listing.objects.filter(
            verification_status=Listing.VERIFICATION_PENDING
        ).count()
        bookings_total = Booking.objects.count()
        return Response(
            {
                "listings": {
                    "approved": approved,
                    "pending_review": pending,
                    "total": Listing.objects.count(),
                },
                "bookings": {"total": bookings_total},
                "time": timezone.now().isoformat(),
            }
        )


class AccountSummaryView(APIView):
    """Authenticated snapshot for owner dashboard widgets (same origin or CORS)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        my_listings = user.listings.count()
        my_bookings_as_owner = Booking.objects.filter(listing__owner=user).count()
        my_bookings_as_renter = Booking.objects.filter(user=user).count()
        return Response(
            {
                "user": {"id": user.id, "username": user.username, "email": user.email},
                "counts": {
                    "my_listings": my_listings,
                    "bookings_on_my_listings": my_bookings_as_owner,
                    "my_rentals": my_bookings_as_renter,
                },
                "time": timezone.now().isoformat(),
            }
        )


class ListingCategoriesView(APIView):
    """Body-style breakdown for approved listings (browse analytics)."""

    permission_classes = [AllowAny]
    authentication_classes: list = []

    def get(self, request):
        rows = (
            Listing.objects.filter(verification_status=Listing.VERIFICATION_APPROVED)
            .values("body_style")
            .annotate(n=Count("id"))
            .order_by("-n")
        )
        return Response(
            {
                "by_body_style": list(rows),
                "time": timezone.now().isoformat(),
            }
        )
