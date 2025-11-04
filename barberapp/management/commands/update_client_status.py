from django.core.management.base import BaseCommand
from barberapp.models import Client

class Command(BaseCommand):
    help = 'Update existing Client records to have a status field'

    def handle(self, *args, **options):
        # Update all existing Client records to have 'pending' status if they don't have one
        clients = Client.objects.all()
        updated_count = 0
        
        for client in clients:
            if not client.status:  # If status is empty or None
                client.status = 'pending'
                client.save()
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} client records with status field'
            )
        )