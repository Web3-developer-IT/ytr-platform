"""Booking totals: rental + deposit, platform commission, owner payout (escrow model)."""
from __future__ import annotations

from decimal import Decimal

from django.conf import settings

from core.models import Listing


def booking_money_snapshot(listing: Listing, *, days: int) -> tuple[Decimal, Decimal, Decimal, Decimal, Decimal]:
    """
    Returns (rental_total, deposit_total, amount_due_total, platform_fee, owner_payout).

    Commission applies to rental portion only. Deposit is held with rental until trip rules are finalized.
    """
    days = max(int(days), 1)
    rental = ((listing.price_per_day or Decimal("0")) * days).quantize(Decimal("0.01"))

    dep_pct = Decimal(str(getattr(settings, "YTR_DEPOSIT_PERCENT", "20")))
    deposit = (rental * dep_pct / Decimal("100")).quantize(Decimal("0.01"))

    total_due = (rental + deposit).quantize(Decimal("0.01"))

    fee_pct = Decimal(str(getattr(settings, "YTR_PLATFORM_COMMISSION_PERCENT", "10")))
    platform_fee = (rental * fee_pct / Decimal("100")).quantize(Decimal("0.01"))
    owner_payout = (rental - platform_fee).quantize(Decimal("0.01"))

    return rental, deposit, total_due, platform_fee, owner_payout
