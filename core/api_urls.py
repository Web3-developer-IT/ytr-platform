from django.urls import path

from . import api_views

urlpatterns = [
    path("health/", api_views.HealthView.as_view(), name="api_health"),
    path("stats/", api_views.PlatformStatsView.as_view(), name="api_platform_stats"),
    path("me/summary/", api_views.AccountSummaryView.as_view(), name="api_account_summary"),
    path("listings/by-style/", api_views.ListingCategoriesView.as_view(), name="api_listings_by_style"),
]
