"""
Curated demo vehicle rows for browse/home when the marketplace is still filling up.
Uses stable HTTPS image URLs (same sources as seed_commercial_listings).
"""

from decimal import Decimal

# Subset for supplemental cards (no DB ids — links go to contact / solutions).
DEMO_BROWSE_CARDS = [
    {
        "title": "Mercedes-Benz Sprinter — crew van",
        "body_style": "Van",
        "location": "Johannesburg, Gauteng",
        "price_per_day": Decimal("1850.00"),
        "image": "https://images.unsplash.com/photo-1549923746-c502d488b3db?auto=format&fit=crop&w=1200&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 3,
    },
    {
        "title": "Toyota Hilux Double Cab — 4x4",
        "body_style": "Bakkie",
        "location": "Port Elizabeth, Eastern Cape",
        "price_per_day": Decimal("1450.00"),
        "image": "https://images.unsplash.com/photo-1559416523-3214c89f6d1e?auto=format&fit=crop&w=1200&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 5,
    },
    {
        "title": "Ford Ranger Wildtrak",
        "body_style": "Bakkie",
        "location": "Stellenbosch, Western Cape",
        "price_per_day": Decimal("1650.00"),
        "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1200&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 5,
    },
    {
        "title": "Isuzu NPR — refrigerated box",
        "body_style": "Commercial",
        "location": "Durban, KwaZulu-Natal",
        "price_per_day": Decimal("3200.00"),
        "image": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1200&q=80",
        "transmission": "Manual",
        "fuel_type": "Diesel",
        "seats": 3,
    },
    {
        "title": "VW Crafter — high roof panel van",
        "body_style": "Van",
        "location": "Cape Town, Western Cape",
        "price_per_day": Decimal("2100.00"),
        "image": "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 3,
    },
    {
        "title": "MAN TGM — curtainside",
        "body_style": "Truck",
        "location": "Pretoria, Gauteng",
        "price_per_day": Decimal("4500.00"),
        "image": "https://images.unsplash.com/photo-1519003722824-194d4455a60c?auto=format&fit=crop&w=1200&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 2,
    },
]
