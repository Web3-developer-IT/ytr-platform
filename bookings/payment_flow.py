"""Escrow lifecycle: expire unpaid approvals, release after trip end, record host payouts."""
from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from .models import Booking, HostPayout


def run_payment_background_jobs() -> tuple[int, int]:
    """
    Run idempotent maintenance: expire overdue payment windows, auto-release escrow + payouts.
    Returns (expired_count, released_count).
    """
    expired = _expire_overdue_payment_pending()
    released = _release_escrow_and_record_payouts()
    return expired, released


def _expire_overdue_payment_pending() -> int:
    now = timezone.now()
    qs = Booking.objects.filter(
        payment_state=Booking.PaymentState.PAYMENT_PENDING,
        payment_due_at__isnull=False,
        payment_due_at__lt=now,
    )
    return qs.update(payment_state=Booking.PaymentState.CANCELLED)


def _release_escrow_and_record_payouts() -> int:
    eligible = Booking.objects.filter(
        payment_state=Booking.PaymentState.IN_ESCROW,
        end_date__lt=timezone.now().date(),
        released_at__isnull=True,
    ).select_related("listing", "listing__owner")

    released = 0
    for booking in eligible:
        with transaction.atomic():
            b = Booking.objects.select_for_update().get(pk=booking.pk)
            if b.payment_state != Booking.PaymentState.IN_ESCROW or b.released_at is not None:
                continue
            now = timezone.now()
            b.payment_state = Booking.PaymentState.RELEASED
            b.released_at = now
            b.save(update_fields=["payment_state", "released_at"])

            HostPayout.objects.get_or_create(
                booking=b,
                defaults={
                    "owner": b.listing.owner,
                    "amount": b.owner_payout_amount or Decimal("0"),
                    "commission_amount": b.platform_fee_amount or Decimal("0"),
                    "status": HostPayout.Status.COMPLETED,
                    "completed_at": now,
                    "notes": "Automatic payout (simulated) — connect PayFast/Yoco for live settlement.",
                },
            )
            released += 1
    return released
