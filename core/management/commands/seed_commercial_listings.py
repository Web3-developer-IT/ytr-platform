"""
Populate the marketplace with commercial / fleet-style listings (vans, trucks, bakkies).
Uses curated Unsplash URLs as hero images. Safe to run multiple times (skips duplicates by title).
"""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from core.models import Listing

# Curated Unsplash images — commercial vehicles & logistics (stable photo IDs).
COMMERCIAL_SEED = [
    {
        "title": "Mercedes-Benz Sprinter LWB — crew van",
        "body_style": "Van",
        "description": "High-roof long-wheelbase panel van. Ideal for crew transport, airport shuttles, and light freight. Daily inspection and full service history.",
        "location": "Johannesburg, Gauteng",
        "price_per_day": Decimal("1850.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1549923746-c502d488b3db?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 3,
        "mileage_km": 142000,
    },
    {
        "title": "Ford Transit Custom — refrigerated",
        "body_style": "Commercial",
        "description": "Temperature-controlled cargo area for catering, pharma samples, or events. Dual sliding doors and tail-lift option on request.",
        "location": "Cape Town, Western Cape",
        "price_per_day": Decimal("2200.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1586191582151-f738f830d2b8?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Manual",
        "fuel_type": "Diesel",
        "seats": 3,
        "mileage_km": 98000,
    },
    {
        "title": "Volkswagen Crafter — high roof",
        "body_style": "Van",
        "description": "Extra-tall cargo bay for palletised loads and fit-out projects. Perfect for film gear, exhibitions, and last-mile logistics.",
        "location": "Durban, KwaZulu-Natal",
        "price_per_day": Decimal("1950.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 3,
        "mileage_km": 118000,
    },
    {
        "title": "Isuzu NPR — dropside truck",
        "body_style": "Truck",
        "description": "3.5t dropside for construction materials, events staging, and agricultural runs. Licensed for commercial loads.",
        "location": "Pretoria, Gauteng",
        "price_per_day": Decimal("2800.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Manual",
        "fuel_type": "Diesel",
        "seats": 3,
        "mileage_km": 205000,
    },
    {
        "title": "Toyota Hilux Double Cab — 4x4",
        "body_style": "Bakkie",
        "description": "Workhorse bakkie with diff lock and tow bar. Suited to site visits, field teams, and weekend adventure fleets.",
        "location": "Port Elizabeth, Eastern Cape",
        "price_per_day": Decimal("1450.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1559416523-3214c89f6d1e?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 5,
        "mileage_km": 87000,
    },
    {
        "title": "Ford Ranger Wildtrak — fleet spec",
        "body_style": "Bakkie",
        "description": "Premium double cab with sports bar and roller shutter. Popular with sales teams and survey crews.",
        "location": "Stellenbosch, Western Cape",
        "price_per_day": Decimal("1650.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 5,
        "mileage_km": 76000,
    },
    {
        "title": "MAN TGL — curtain side",
        "body_style": "Truck",
        "description": "12-tonne curtain-sider for palletised freight and retail distribution. Tail-lift and load-secure bars included.",
        "location": "Germiston, Gauteng",
        "price_per_day": Decimal("4200.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 2,
        "mileage_km": 312000,
    },
    {
        "title": "Iveco Daily — panel van",
        "body_style": "Van",
        "description": "Compact city van with excellent turning circle. Courier, samples, and same-day delivery friendly.",
        "location": "Sandton, Gauteng",
        "price_per_day": Decimal("1250.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Manual",
        "fuel_type": "Diesel",
        "seats": 3,
        "mileage_km": 154000,
    },
    {
        "title": "Mercedes-Benz Vito Tourer — 8 seats",
        "body_style": "Fleet",
        "description": "Executive people-mover for shuttles, conferences, and crew moves. Leather trim and rear climate.",
        "location": "Umhlanga, KwaZulu-Natal",
        "price_per_day": Decimal("2100.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 8,
        "mileage_km": 99000,
    },
    {
        "title": "Fuso Canter — box body",
        "body_style": "Commercial",
        "description": "Enclosed box body for furniture moves and fragile freight. Ramp and trolley available.",
        "location": "Midrand, Gauteng",
        "price_per_day": Decimal("2650.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1519003722824-c3048a45d4ae?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Manual",
        "fuel_type": "Diesel",
        "seats": 3,
        "mileage_km": 178000,
    },
    {
        "title": "Nissan NP300 — single cab workhorse",
        "body_style": "Bakkie",
        "description": "Light commercial bakkie for trades and municipal teams. Canopy and rack options.",
        "location": "Bloemfontein, Free State",
        "price_per_day": Decimal("890.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1629897048514-3dd7414fe72a?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Manual",
        "fuel_type": "Diesel",
        "seats": 2,
        "mileage_km": 201000,
    },
    {
        "title": "Scania P-series — rigid freight",
        "body_style": "Truck",
        "description": "Heavy rigid for regional line-haul and warehouse transfers. Experienced operators only.",
        "location": "Richards Bay, KwaZulu-Natal",
        "price_per_day": Decimal("5100.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 2,
        "mileage_km": 428000,
    },
    {
        "title": "Renault Master — Luton low-loader",
        "body_style": "Van",
        "description": "Wide Luton-style body for bulky retail and white-glove deliveries. Ideal for e-commerce peaks.",
        "location": "Centurion, Gauteng",
        "price_per_day": Decimal("1750.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1566576721346-d4a3b4eaeb55?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Manual",
        "fuel_type": "Diesel",
        "seats": 3,
        "mileage_km": 133000,
    },
    {
        "title": "Volkswagen Amarok — fleet double cab",
        "body_style": "Fleet",
        "description": "Refined 4x4 double cab for mixed road and gravel. Popular with inspection and engineering teams.",
        "location": "George, Western Cape",
        "price_per_day": Decimal("1550.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 5,
        "mileage_km": 112000,
    },
    {
        "title": "Hino 300 — refrigerated truck",
        "body_style": "Commercial",
        "description": "Cold-chain truck for food service and medical logistics. Telemetry and temp logging on board.",
        "location": "Polokwane, Limpopo",
        "price_per_day": Decimal("3400.00"),
        "hero_image_url": "https://images.unsplash.com/photo-1516937941344-00b4e0337589?auto=format&fit=crop&w=1600&q=80",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 3,
        "mileage_km": 256000,
    },
]


class Command(BaseCommand):
    help = "Create commercial / fleet demo listings (skips existing titles)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--purge-titles",
            action="store_true",
            help="Delete existing seed titles before insert (use with care).",
        )

    def handle(self, *args, **options):
        owner, _ = User.objects.get_or_create(
            username="ytr_fleet_demo",
            defaults={
                "email": "fleet.demo@yourstorent.local",
                "first_name": "YTR",
                "last_name": "Fleet Demo",
            },
        )
        if not owner.has_usable_password():
            owner.set_unusable_password()
            owner.save(update_fields=["password"])

        if options["purge_titles"]:
            titles = [row["title"] for row in COMMERCIAL_SEED]
            deleted, _ = Listing.objects.filter(title__in=titles).delete()
            self.stdout.write(self.style.WARNING(f"Removed existing seed listings (cascade): {deleted}"))

        created = 0
        skipped = 0
        for row in COMMERCIAL_SEED:
            if Listing.objects.filter(title=row["title"]).exists():
                skipped += 1
                continue
            Listing.objects.create(
                owner=owner,
                title=row["title"],
                description=row["description"],
                category="car",
                body_style=row["body_style"],
                location=row["location"],
                price_per_day=row["price_per_day"],
                available=True,
                verification_status=Listing.VERIFICATION_APPROVED,
                hero_image_url=row["hero_image_url"],
                transmission=row["transmission"],
                fuel_type=row["fuel_type"],
                seats=row["seats"],
                mileage_km=row["mileage_km"],
            )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Commercial seed complete: {created} created, {skipped} already present. Owner: {owner.username}"
            )
        )
