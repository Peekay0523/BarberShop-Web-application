import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from django.contrib.auth.models import User
from barberapp.models import Customer

def create_test_user():
    # Check if test user already exists
    if not User.objects.filter(username='testuser').exists():
        # Create a regular test user (not a superuser)
        test_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        
        # Add first and last name
        test_user.first_name = 'Test'
        test_user.last_name = 'User'
        test_user.save()
        
        print('Test user created successfully!')
        print(f'Username: {test_user.username}')
        print(f'Email: {test_user.email}')
        print(f'Password: testpassword123')
        
        # Create a customer profile for the user
        try:
            customer, created = Customer.objects.get_or_create(user=test_user)
            if created:
                print('Customer profile created for test user!')
            else:
                print('Customer profile already existed for test user.')
        except Exception as e:
            print(f'Error creating customer profile: {e}')
        
    else:
        print('Test user already exists!')
        test_user = User.objects.get(username='testuser')
        print(f'Username: {test_user.username}')
        print(f'Email: {test_user.email}')

if __name__ == '__main__':
    create_test_user()