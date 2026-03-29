from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    CATEGORY_CHOICES = (
        ("car", "Car"),
        ("tool", "Tool"),
        ("equipment", "Equipment"),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="car")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    VERIFICATION_PENDING = "pending"
    VERIFICATION_APPROVED = "approved"
    VERIFICATION_REJECTED = "rejected"
    VERIFICATION_CHOICES = (
        (VERIFICATION_PENDING, "Pending review"),
        (VERIFICATION_APPROVED, "Approved"),
        (VERIFICATION_REJECTED, "Rejected"),
    )
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_CHOICES,
        default=VERIFICATION_APPROVED,
        db_index=True,
        help_text="Admin approval before a listing appears in browse/search.",
    )

    # Display / browse card fields (used across browse + detail)
    body_style = models.CharField(
        max_length=64,
        default="Sedan",
        help_text="Shown on cards (e.g. Luxury, SUV, Bakkie).",
    )
    transmission = models.CharField(max_length=32, default="Automatic")
    fuel_type = models.CharField(max_length=32, default="Petrol")
    seats = models.PositiveSmallIntegerField(default=5)
    mileage_km = models.PositiveIntegerField(default=0)
    hero_image_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Optional hero image when no uploaded ListingImage exists.",
    )

    def __str__(self):
        return self.title

    def primary_image_url(self):
        first = self.images.order_by("uploaded_at").first()
        if first and first.image:
            return first.image.url
        return self.hero_image_url or ""

    def mileage_display(self):
        if not self.mileage_km:
            return "—"
        if self.mileage_km >= 1000:
            return f"{self.mileage_km // 1000}k km"
        return f"{self.mileage_km} km"

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    # Stored under vehicles/ in Cloudinary (and local media) for consistent investor-facing URLs.
    image = models.ImageField(upload_to="vehicles/listings")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.listing.title}"