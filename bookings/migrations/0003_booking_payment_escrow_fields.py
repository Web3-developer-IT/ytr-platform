from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0002_booking_created_at_alter_booking_listing_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="payment_state",
            field=models.CharField(
                max_length=32,
                default="awaiting_host",
                choices=[
                    ("awaiting_host", "Awaiting host approval"),
                    ("payment_pending", "Approved — payment due"),
                    ("in_escrow", "Funds held in YTR escrow"),
                    ("released", "Released to host"),
                    ("cancelled", "Cancelled"),
                ],
            ),
        ),
        migrations.AddField(
            model_name="booking",
            name="payment_due_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="rental_total",
            field=models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0")),
        ),
        migrations.AddField(
            model_name="booking",
            name="deposit_total",
            field=models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0")),
        ),
        migrations.AddField(
            model_name="booking",
            name="amount_due_total",
            field=models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0")),
        ),
        migrations.AddField(
            model_name="booking",
            name="platform_fee_amount",
            field=models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0")),
        ),
        migrations.AddField(
            model_name="booking",
            name="owner_payout_amount",
            field=models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0")),
        ),
    ]
