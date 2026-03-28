from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    PROPERTY_TYPES = (
        ('store', 'Store'),
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('warehouse', 'Warehouse'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title