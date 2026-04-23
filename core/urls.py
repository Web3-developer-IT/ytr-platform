from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views

# Removed from public site (redirect to home). Names preserved for {% url %} compatibility.
_REDIRECT_HOME = RedirectView.as_view(url="/", permanent=False)

urlpatterns = [
    # Legacy static filenames (must be before 'listings/' and '<int:listing_id>' patterns)
    path('listings/vehicle-details.html', views.listing_detail_fallback, name='listings_vehicle_details_html'),
    path('listings/index.html', views.home, name='listings_index_html'),

    path('', views.home, name='home'),
    path('index.html', views.home),
    path('about/', views.about, name='about'),
    path('about.html', views.about),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('how-it-works.html', views.how_it_works),
    path('contact/', views.contact, name='contact'),
    path('contact.html', views.contact),
    path('services/', _REDIRECT_HOME, name='services'),
    path('services.html', _REDIRECT_HOME),
    path('feedback/', views.feedback_page, name='feedback'),
    path('feedback.html', views.feedback_page),
    path('faq/', views.faq_page, name='faq'),
    path('faq.html', views.faq_page),

    path('terms/', views.terms_page, name='terms'),
    path('terms.html', views.terms_page),
    path('privacy/', views.privacy_page, name='privacy'),
    path('privacy.html', views.privacy_page),
    path('cookies/', views.cookies_page, name='cookies'),
    path('cookies.html', views.cookies_page),
    path('careers/', views.careers_page, name='careers'),
    path('careers.html', views.careers_page),
    path('partners/', views.partners_marketing_page, name='partners'),
    path('partners.html', views.partners_marketing_page),
    path('insurance/', views.insurance_page, name='insurance'),
    path('insurance.html', views.insurance_page),
    path('trust-safety/', views.trust_safety_public_page, name='trust_safety'),
    path('trust-safety.html', views.trust_safety_public_page),
    path('solutions/fleet/', _REDIRECT_HOME, name='fleet_solutions'),
    path('solutions/mobility/', _REDIRECT_HOME, name='mobility_hub'),
    path('solutions/dispatch/', _REDIRECT_HOME, name='dispatch_console'),
    path('solutions/partners/', views.partner_network, name='partner_network'),
    path('solutions/trust-center/', _REDIRECT_HOME, name='trust_center'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),

    path('listings/', views.listings_page, name='listings'),
    path('browse/', views.listings_page, name='browse'),
    path('browse.html', views.listings_page),
    path('browse/vehicle-details.html', views.listing_detail_fallback, name='browse_vehicle_details_fallback'),
    path('how-it-works/browse.html', views.listings_page, name='how_it_works_browse_html'),

    # Legacy static export used "messages/index.html" — was incorrectly routed to home; send users to inbox.
    path(
        'messages/index.html',
        RedirectView.as_view(url='/messages/', permanent=False),
        name='messages_index_html_redirect',
    ),

    path('listings/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('vehicle-details.html', views.listing_detail_fallback, name='vehicle_details_fallback'),
    re_path(
        r'^(browse|dashboard|messages|profile|settings|my-bookings|my-vehicles|earnings|transactions|payouts|help-center)/vehicle-details\.html$',
        views.listing_detail_fallback,
    ),
    # Excludes "messages" — handled above so /messages/ inbox works (see messages_index_html_redirect).
    re_path(
        r'^(browse|dashboard|profile|settings|my-bookings|my-vehicles|earnings|transactions|payouts|help-center)/index\.html$',
        views.home,
    ),

    path('listings/<int:listing_id>/book/', views.book_listing, name='book_listing'),
    path('bookings/<int:booking_id>/checkout/', views.booking_checkout, name='booking_checkout'),

    path('search/', views.search_listings, name='search_listings'),

    path('dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('dashboard.html', views.owner_dashboard),
    path('my-bookings/', views.my_bookings_page, name='my_bookings'),
    path('my-bookings.html', views.my_bookings_page),
    path('my-vehicles/', views.my_vehicles_page, name='my_vehicles'),
    path('my-vehicles.html', views.my_vehicles_page),
    path('earnings/', views.earnings_page, name='earnings'),
    path('earnings.html', views.earnings_page),
    path('transactions/', views.transactions_page, name='transactions'),
    path('transactions.html', views.transactions_page),
    path('payouts/', views.payouts_page, name='payouts'),
    path('payouts.html', views.payouts_page),
    path('help-center/', views.help_center_page, name='help_center'),
    path('help-center.html', views.help_center_page),
    path('profile/', views.profile_page, name='profile'),
    path('profile.html', views.profile_page),
    path('settings/', views.settings_page, name='settings'),
    path('settings.html', views.settings_page),

    path('booking/approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    # Listing actions (+ prototype alias)
    path('listing/add/', views.add_listing, name='add_listing'),
    path('list-vehicle/', views.add_listing),
    path('list-vehicle.html', views.add_listing),
    path('listing/edit/<int:listing_id>/', views.edit_listing, name='edit_listing'),
    path('listing/delete/<int:listing_id>/', views.delete_listing, name='delete_listing'),

]