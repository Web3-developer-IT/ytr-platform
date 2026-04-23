"""
Normalize image URLs so they work behind HTTPS proxies (Render), mixed content, and protocol-relative URLs.
"""

from django.conf import settings


def normalize_image_url(url) -> str:
    if not url or not str(url).strip():
        return ""
    u = str(url).strip()
    # Legacy static exports / broken relative paths → use listing fallbacks instead.
    if u.startswith("./images/") or (u.startswith("images/") and "://" not in u and not u.startswith("/media/")):
        return ""
    if u.startswith("//"):
        return "https:" + u
    # Upgrade http→https for third-party CDNs (fixes broken previews on HTTPS hosts like Render).
    if u.startswith("http://") and "127.0.0.1" not in u and "localhost" not in u:
        u = "https://" + u[7:]
    return u


def best_listing_image_url(listing) -> str:
    """Uploaded Cloudinary/local → hero URL → global default → rotating fallbacks."""
    raw = ""
    try:
        p = getattr(listing, "primary_image_url", None)
        raw = p() if callable(p) else (p or "")
    except Exception:
        raw = ""
    raw = normalize_image_url(raw)
    if raw:
        return raw
    fallback = normalize_image_url(getattr(settings, "YTR_DEFAULT_VEHICLE_IMAGE_URL", "") or "")
    if fallback:
        return fallback
    alts = getattr(settings, "YTR_IMAGE_FALLBACK_URLS", None) or []
    if alts:
        idx = (getattr(listing, "id", 0) or 0) % len(alts)
        return normalize_image_url(alts[idx]) or str(alts[0])
    return ""
