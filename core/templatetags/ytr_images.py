from django import template
from django.conf import settings

from core.ytr_media import best_listing_image_url, normalize_image_url

register = template.Library()


@register.filter
def ytr_img(url):
    """Normalize a single image URL for <img src>."""
    n = normalize_image_url(url or "")
    return n or normalize_image_url(getattr(settings, "YTR_DEFAULT_VEHICLE_IMAGE_URL", "") or "")


@register.simple_tag
def listing_card_image(listing):
    """Best URL for marketplace cards (Cloudinary upload, hero, or fallbacks)."""
    return best_listing_image_url(listing)
