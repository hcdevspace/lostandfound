from django.core.management.base import BaseCommand
from django.utils import timezone
from items.models import Item
from claims.models import Claim
from accounts.emails import send_item_discarded_email


class Command(BaseCommand):
    help = 'Automatically discard items that have been unclaimed for a specified number of days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Number of days after which to auto-discard items (default: 90)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be discarded without actually discarding',
        )

    def handle(self, *args, **options):
        threshold_days = options['days']
        dry_run = options['dry_run']

        # Find items eligible for auto-discard
        eligible_items = Item.objects.filter(
            status__in=['unclaimed', 'rejected']
        )

        items_to_discard = [
            item for item in eligible_items
            if item.is_eligible_for_auto_discard(threshold_days)
        ]

        if not items_to_discard:
            self.stdout.write(
                self.style.SUCCESS(f'No items found that are unclaimed for {threshold_days}+ days.')
            )
            return

        self.stdout.write(
            self.style.WARNING(f'Found {len(items_to_discard)} items eligible for auto-discard:')
        )

        for item in items_to_discard:
            days_old = item.days_since_reported()
            self.stdout.write(
                f'  - {item.name} (ID: {item.pk}) - {days_old} days old - Status: {item.status}'
            )

        if dry_run:
            self.stdout.write(
                self.style.WARNING('\n[DRY RUN] No items were actually discarded.')
            )
            return

        # Perform the discard
        discard_count = 0
        for item in items_to_discard:
            item.status = 'discarded'
            item.discard_date = timezone.now()
            item.discard_reason = f'Auto-discarded: Unclaimed for {threshold_days}+ days'
            item.save()

            # Notify the original reporter
            if item.submitted_by and item.submitted_by.email:
                send_item_discarded_email(item.submitted_by, item)

            # Notify any active claimant (different from the reporter)
            active_claim = Claim.objects.filter(
                item=item, status__in=['pending', 'approved']
            ).select_related('claimant').first()
            if (active_claim and active_claim.claimant.email and
                    active_claim.claimant != item.submitted_by):
                send_item_discarded_email(active_claim.claimant, item)

            discard_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully auto-discarded {discard_count} items.')
        )