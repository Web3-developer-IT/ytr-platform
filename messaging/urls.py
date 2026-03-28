from django.urls import path
from . import views

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path(
        "conversation/<int:listing_id>/<int:user_id>/",
        views.conversation,
        name="conversation"
    ),
]
