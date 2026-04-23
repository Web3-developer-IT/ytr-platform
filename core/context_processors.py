from django.conf import settings
from django.templatetags.static import static


def ytr_branding(request):
    """Default imagery + branding values available in all templates."""
    logo_path = getattr(settings, "YTR_LOGO_STATIC_PATH", "images/nikki.png")
    return {
        "ytr_default_vehicle_image": getattr(
            settings,
            "YTR_DEFAULT_VEHICLE_IMAGE_URL",
            "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=900&q=80",
        ),
        "ytr_static_cdn_base": getattr(settings, "YTR_STATIC_CDN_BASE", "") or "",
        "ytr_platform_version": getattr(settings, "YTR_PLATFORM_VERSION", "1.0.0"),
        "ytr_logo_url": static(logo_path),
        "ytr_payment_deadline_days": int(getattr(settings, "YTR_PAYMENT_DEADLINE_DAYS", 5)),
        "ytr_commission_percent": str(getattr(settings, "YTR_PLATFORM_COMMISSION_PERCENT", "10")),
    }
