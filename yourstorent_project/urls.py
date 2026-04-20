from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings

admin.site.site_header = "Yours To Rent — Control Panel"
admin.site.site_title = "YTR Admin"
admin.site.index_title = "Manage listings, users, documents & notifications"
from django.conf.urls.static import static
from django.views.static import serve
import os
from core import views as core_views


urlpatterns = [

    path('admin/', admin.site.urls),

    path("api/v1/", include("core.api_urls")),

    path('oauth/', include('allauth.urls')),

    path('', include('core.urls')),

    path('', include('accounts.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('users.urls')),
    path('users/', include('users.urls')),

    path("messages/", include("messaging.urls")),
    re_path(r"^media/(?P<path>.*)$", core_views.media_with_fallback, name="media_with_fallback"),

    # Prototype asset compatibility for /download HTML references
    re_path(r"^css/(?P<path>.*)$", serve, {"document_root": os.path.join(settings.BASE_DIR, "static", "css")}),
    re_path(r"^js/(?P<path>.*)$", serve, {"document_root": os.path.join(settings.BASE_DIR, "static", "js")}),
    re_path(r"^images/(?P<path>.*)$", serve, {"document_root": os.path.join(settings.BASE_DIR, "static", "images")}),

]


if settings.DEBUG or not getattr(settings, "YTR_USE_CLOUDINARY", False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
