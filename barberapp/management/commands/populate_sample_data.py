from django.core.management.base import BaseCommand
from barberapp.models import Barber, Service

class Command(BaseCommand):
    help = 'Populate database with sample barbers and services'

    def handle(self, *args, **options):
        # Create sample barbers
        barbers_data = [
            {
                'name': 'John Smith',
                'specialty': 'Classic Cuts',
                'experience': 10
            },
            {
                'name': 'Mike Johnson',
                'specialty': 'Modern Styles',
                'experience': 8
            },
            {
                'name': 'David Wilson',
                'specialty': 'Beard Trimming',
                'experience': 12
            }
        ]
        
        for barber_data in barbers_data:
            barber, created = Barber.objects.get_or_create(
                name=barber_data['name'],
                defaults={
                    'specialty': barber_data['specialty'],
                    'experience': barber_data['experience']
                }
            )
            if created:
                self.stdout.write(f"Created barber: {barber.name}")
            else:
                self.stdout.write(f"Barber already exists: {barber.name}")
        
        # Create sample services
        services_data = [
            {
                'name': 'Classic Haircut',
                'description': 'Traditional haircut with scissor and comb',
                'price': 30.00,
                'duration': 30
            },
            {
                'name': 'Beard Trim',
                'description': 'Precision beard trimming and shaping',
                'price': 20.00,
                'duration': 20
            },
            {
                'name': 'Haircut & Beard',
                'description': 'Complete grooming package',
                'price': 45.00,
                'duration': 45
            },
            {
                'name': 'Hot Towel Shave',
                'description': 'Luxurious hot towel shave experience',
                'price': 25.00,
                'duration': 30
            },
            {
                'name': 'Haircut & Hot Towel',
                'description': 'Haircut followed by hot towel treatment',
                'price': 50.00,
                'duration': 50
            }
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'description': service_data['description'],
                    'price': service_data['price'],
                    'duration': service_data['duration']
                }
            )
            if created:
                self.stdout.write(f"Created service: {service.name}")
            else:
                self.stdout.write(f"Service already exists: {service.name}")
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample data')
        )