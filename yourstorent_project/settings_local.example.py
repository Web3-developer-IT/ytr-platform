"""
Copy to settings_local.py on the VPS (do not commit settings_local.py).
"""

# SECURITY: always set a long, random secret in production.
SECRET_KEY = "replace-me-with-a-long-random-secret"

# Production should be False.
DEBUG = False

# Add your real domains / hostnames.
ALLOWED_HOSTS = [
    "yourstorent.co.za",
    "www.yourstorent.co.za",
    "srv1549778.hstgr.cloud",
]

# If you terminate TLS at nginx/reverse-proxy.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Example: explicit logo path override.
YTR_LOGO_STATIC_PATH = "images/nikki.png"
