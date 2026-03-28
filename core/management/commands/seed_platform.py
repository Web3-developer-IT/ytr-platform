from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import Listing


DEMO_LISTINGS = [
    {
        "title": "Mercedes-Benz S-Class",
        "description": "Flagship luxury sedan in excellent condition — ideal for executive travel along the KZN coast.",
        "location": "Umhlanga, Durban",
        "price_per_day": Decimal("3200.00"),
        "category": "car",
        "body_style": "Luxury",
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "seats": 5,
        "mileage_km": 12000,
        "hero_image_url": "https://images.unsplash.com/photo-1617469767053-d3b523a0b982?w=1200",
    },
    {
        "title": "BMW 3 Series 330i M Sport",
        "description": "Premium sports sedan with balanced performance for city and highway driving.",
        "location": "Sandton, Johannesburg",
        "price_per_day": Decimal("1250.00"),
        "category": "car",
        "body_style": "Sedan",
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "seats": 5,
        "mileage_km": 45000,
        "hero_image_url": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=1200",
    },
    {
        "title": "Mercedes-Benz GLE 2022",
        "description": "Spacious luxury SUV with commanding presence and comfort for family trips.",
        "location": "Cape Town City Centre",
        "price_per_day": Decimal("1450.00"),
        "category": "car",
        "body_style": "SUV",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 7,
        "mileage_km": 32000,
        "hero_image_url": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=1200",
    },
    {
        "title": "Ford Mustang GT",
        "description": "Iconic V8 muscle — unforgettable weekend drives.",
        "location": "Umhlanga, Durban",
        "price_per_day": Decimal("1200.00"),
        "category": "car",
        "body_style": "Sports",
        "transmission": "Manual",
        "fuel_type": "Petrol",
        "seats": 4,
        "mileage_km": 28000,
        "hero_image_url": "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=1200",
    },
    {
        "title": "Toyota Hilux Legend 50",
        "description": "Tough double-cab bakkie — work-ready and adventure-capable.",
        "location": "Centurion, Pretoria",
        "price_per_day": Decimal("750.00"),
        "category": "car",
        "body_style": "Bakkie",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 5,
        "mileage_km": 65000,
        "hero_image_url": "https://images.unsplash.com/photo-1609521263047-f8f205293f24?w=1200",
    },
    {
        "title": "Volkswagen Polo TSI",
        "description": "Economical and nimble — perfect for urban commuting.",
        "location": "Hatfield, Pretoria",
        "price_per_day": Decimal("450.00"),
        "category": "car",
        "body_style": "Economy",
        "transmission": "Manual",
        "fuel_type": "Petrol",
        "seats": 5,
        "mileage_km": 52000,
        "hero_image_url": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=1200",
    },
    {
        "title": "Audi Q7 55 TFSI",
        "description": "Premium seven-seater SUV with quattro confidence.",
        "location": "Rosebank, Johannesburg",
        "price_per_day": Decimal("1850.00"),
        "category": "car",
        "body_style": "SUV",
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "seats": 7,
        "mileage_km": 38000,
        "hero_image_url": "https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=1200",
    },
    {
        "title": "Range Rover Vogue",
        "description": "Refined luxury SUV with commanding road presence.",
        "location": "Clifton, Cape Town",
        "price_per_day": Decimal("2800.00"),
        "category": "car",
        "body_style": "Luxury SUV",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 5,
        "mileage_km": 25000,
        "hero_image_url": "https://images.unsplash.com/photo-1542362567-b07e54358753?w=1200",
    },
    {
        "title": "Toyota Corolla Cross",
        "description": "Practical hybrid crossover with excellent fuel economy.",
        "location": "Menlyn, Pretoria",
        "price_per_day": Decimal("650.00"),
        "category": "car",
        "body_style": "SUV",
        "transmission": "Automatic",
        "fuel_type": "Hybrid",
        "seats": 5,
        "mileage_km": 18000,
        "hero_image_url": "https://images.unsplash.com/photo-1502877338535-766e1452684a?w=1200",
    },
    {
        "title": "Ford Ranger Wildtrak",
        "description": "Premium bakkie with smart tech and strong towing capability.",
        "location": "Ballito, Durban",
        "price_per_day": Decimal("850.00"),
        "category": "car",
        "body_style": "Bakkie",
        "transmission": "Automatic",
        "fuel_type": "Diesel",
        "seats": 5,
        "mileage_km": 42000,
        "hero_image_url": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=1200",
    },
    {
        "title": "Chevrolet Corvette C8",
        "description": "Mid-engine American supercar experience.",
        "location": "V&A Waterfront, Cape Town",
        "price_per_day": Decimal("4200.00"),
        "category": "car",
        "body_style": "Sports",
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "seats": 2,
        "mileage_km": 8000,
        "hero_image_url": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=1200",
    },
    {
        "title": "Porsche 911 Carrera",
        "description": "Precision handling and timeless design.",
        "location": "Camps Bay, Cape Town",
        "price_per_day": Decimal("3500.00"),
        "category": "car",
        "body_style": "Luxury",
        "transmission": "Automatic",
        "fuel_type": "Petrol",
        "seats": 2,
        "mileage_km": 15000,
        "hero_image_url": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=1200",
    },
]


class Command(BaseCommand):
    help = "Create demo host user and sample vehicle listings (safe to re-run)."

    def handle(self, *args, **options):
        host, created = User.objects.get_or_create(
            username="demo_host",
            defaults={
                "email": "host@yourstorent.co.za",
                "first_name": "Michael",
                "last_name": "Host",
            },
        )
        if created or not host.has_usable_password():
            host.set_password("demo1234")
            host.save()

        count = 0
        for row in DEMO_LISTINGS:
            _obj, was_created = Listing.objects.update_or_create(
                owner=host,
                title=row["title"],
                defaults={
                    "description": row["description"],
                    "location": row["location"],
                    "price_per_day": row["price_per_day"],
                    "category": row["category"],
                    "body_style": row["body_style"],
                    "transmission": row["transmission"],
                    "fuel_type": row["fuel_type"],
                    "seats": row["seats"],
                    "mileage_km": row["mileage_km"],
                    "hero_image_url": row["hero_image_url"],
                    "available": True,
                },
            )
            if was_created:
                count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo listings ready (host: demo_host / demo1234). New rows this run: {count}."
            )
        )
