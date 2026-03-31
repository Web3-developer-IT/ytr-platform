from django.conf import settings


def ytr_branding(request):
    """Default imagery + branding values available in all templates."""
    return {
        "ytr_default_vehicle_image": getattr(
            settings,
            "YTR_DEFAULT_VEHICLE_IMAGE_URL",
            "/static/images/hero-cars-reference.png",
        ),
    }
