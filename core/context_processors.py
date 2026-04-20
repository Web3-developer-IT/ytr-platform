from django.conf import settings


def ytr_branding(request):
    """Default imagery + branding values available in all templates."""
    return {
        "ytr_default_vehicle_image": getattr(
            settings,
            "YTR_DEFAULT_VEHICLE_IMAGE_URL",
            "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=900&q=80",
        ),
        "ytr_static_cdn_base": getattr(settings, "YTR_STATIC_CDN_BASE", "") or "",
        "ytr_platform_version": getattr(settings, "YTR_PLATFORM_VERSION", "1.0.0"),
    }
