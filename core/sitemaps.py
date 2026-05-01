from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from core.models import Listing


class StaticViewSitemap(Sitemap):
    protocol = "https"
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "browse",
            "about",
            "how_it_works",
            "contact",
            "faq",
            "terms",
            "privacy",
            "cookies",
            "careers",
            "partners",
            "insurance",
            "trust_safety",
        ]

    def location(self, item):
        return reverse(item)


class ListingSitemap(Sitemap):
    protocol = "https"
    priority = 0.8
    changefreq = "daily"

    def items(self):
        return Listing.objects.filter(
            available=True,
            verification_status=Listing.VERIFICATION_APPROVED,
        ).order_by("-created_at")

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse("listing_detail", args=[obj.id])


sitemaps = {
    "pages": StaticViewSitemap,
    "listings": ListingSitemap,
}
