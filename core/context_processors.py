from django.conf import settings
from django.contrib.staticfiles import finders
from django.urls import reverse
from django.templatetags.static import static


def ytr_branding(request):
    """Default imagery + branding values available in all templates."""
    logo_path = getattr(settings, "YTR_LOGO_STATIC_PATH", "images/nikki.png")
    # Safety net for deployments where new static assets were not collected yet.
    if not finders.find(logo_path):
        logo_path = "images/ytr-logo-reference.svg"
    return {
        "ytr_default_vehicle_image": getattr(
            settings,
            "YTR_DEFAULT_VEHICLE_IMAGE_URL",
            "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=900&q=80",
        ),
        "ytr_static_cdn_base": getattr(settings, "YTR_STATIC_CDN_BASE", "") or "",
        "ytr_platform_version": getattr(settings, "YTR_PLATFORM_VERSION", "1.0.0"),
        "ytr_site_url": getattr(settings, "YTR_SITE_URL", "https://yourstorent.co.za").rstrip("/"),
        # Prefer dynamic endpoint so logo always resolves on production even
        # when static mappings differ across hosts.
        "ytr_logo_url": reverse("platform_logo"),
        "ytr_logo_static_url": static(logo_path),
        "ytr_payment_deadline_days": int(getattr(settings, "YTR_PAYMENT_DEADLINE_DAYS", 5)),
        "ytr_commission_percent": str(getattr(settings, "YTR_PLATFORM_COMMISSION_PERCENT", "10")),
    }
