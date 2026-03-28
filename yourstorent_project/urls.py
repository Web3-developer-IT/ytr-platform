from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings

admin.site.site_header = "Yours To Rent — Control Panel"
admin.site.site_title = "YTR Admin"
admin.site.index_title = "Manage listings, users, documents & notifications"
from django.conf.urls.static import static
from django.views.static import serve
import os


urlpatterns = [

    path('admin/', admin.site.urls),

    path('oauth/', include('allauth.urls')),

    path('', include('core.urls')),

    path('', include('accounts.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('users.urls')),
    path('users/', include('users.urls')),

    path("messages/", include("messaging.urls")),

    # Prototype asset compatibility for /download HTML references
    re_path(r"^css/(?P<path>.*)$", serve, {"document_root": os.path.join(settings.BASE_DIR, "static", "css")}),
    re_path(r"^js/(?P<path>.*)$", serve, {"document_root": os.path.join(settings.BASE_DIR, "static", "js")}),
    re_path(r"^images/(?P<path>.*)$", serve, {"document_root": os.path.join(settings.BASE_DIR, "static", "images")}),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)