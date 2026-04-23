from django.db import models
from django.contrib.auth.models import User
from core.models import Listing


class Booking(models.Model):
    """Rental booking with approval + timed payment (escrow) workflow."""

    class PaymentState(models.TextChoices):
        AWAITING_HOST = "awaiting_host", "Awaiting host approval"
        PAYMENT_PENDING = "payment_pending", "Approved — payment due"
        IN_ESCROW = "in_escrow", "Funds held in YTR escrow"
        RELEASED = "released", "Released to host"
        CANCELLED = "cancelled", "Cancelled"

    class PaymentMethod(models.TextChoices):
        CARD = "card", "Card (on-site checkout)"
        EFT = "eft", "EFT (bank transfer)"

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    payment_state = models.CharField(
        max_length=32,
        choices=PaymentState.choices,
        default=PaymentState.AWAITING_HOST,
    )
    payment_due_at = models.DateTimeField(blank=True, null=True)
    rental_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deposit_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_due_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    platform_fee_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    owner_payout_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    payment_method = models.CharField(
        max_length=16,
        choices=PaymentMethod.choices,
        blank=True,
        default="",
    )
    paid_at = models.DateTimeField(blank=True, null=True)
    released_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.listing.title} booked by {self.user.username}"


class HostPayout(models.Model):
    """Automatic host settlement after escrow release (commission stored separately)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed (automated)"

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="host_payout")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="host_payouts")
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Net to host after platform commission on rental.",
    )
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.COMPLETED)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Payout {self.booking_id} → {self.owner_id} R{self.amount}"