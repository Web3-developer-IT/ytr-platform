from django.core.management.base import BaseCommand

from bookings.payment_flow import run_payment_background_jobs


class Command(BaseCommand):
    help = "Expire unpaid bookings, release escrow after trip end, record automatic host payouts."

    def handle(self, *args, **options):
        expired, released = run_payment_background_jobs()
        self.stdout.write(self.style.SUCCESS(f"Expired payment windows: {expired}; escrow releases: {released}"))
