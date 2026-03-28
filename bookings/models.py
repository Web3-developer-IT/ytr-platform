from django.db import models
from django.contrib.auth.models import User
from core.models import Listing

class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} booked by {self.user.username}"