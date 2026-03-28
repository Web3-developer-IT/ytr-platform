from django.urls import path

from . import views

urlpatterns = [
    path("documents/", views.documents_center, name="documents_center"),
    path(
        "notifications/<int:notification_id>/read/",
        views.mark_notification_read,
        name="mark_notification_read",
    ),
]
