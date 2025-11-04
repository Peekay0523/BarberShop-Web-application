import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

from django.contrib.auth.models import User
from barberapp.models import Customer

def create_additional_test_users():
    # Create second test user
    if not User.objects.filter(username='johndoe').exists():
        test_user2 = User.objects.create_user(
            username='johndoe',
            email='johndoe@example.com',
            password='johndoe123'
        )
        
        test_user2.first_name = 'John'
        test_user2.last_name = 'Doe'
        test_user2.save()
        
        print('Second test user created successfully!')
        print(f'Username: {test_user2.username}')
        print(f'Email: {test_user2.email}')
        print(f'Password: johndoe123')
        
        # Create a customer profile for the second user
        try:
            customer, created = Customer.objects.get_or_create(user=test_user2)
            if created:
                print('Customer profile created for second test user!')
            else:
                print('Customer profile already existed for second test user.')
        except Exception as e:
            print(f'Error creating customer profile: {e}')
    else:
        print('Second test user already exists!')
        
    # Create third test user
    if not User.objects.filter(username='janedoe').exists():
        test_user3 = User.objects.create_user(
            username='janedoe',
            email='janedoe@example.com',
            password='janedoe123'
        )
        
        test_user3.first_name = 'Jane'
        test_user3.last_name = 'Doe'
        test_user3.save()
        
        print('Third test user created successfully!')
        print(f'Username: {test_user3.username}')
        print(f'Email: {test_user3.email}')
        print(f'Password: janedoe123')
        
        # Create a customer profile for the third user
        try:
            customer, created = Customer.objects.get_or_create(user=test_user3)
            if created:
                print('Customer profile created for third test user!')
            else:
                print('Customer profile already existed for third test user.')
        except Exception as e:
            print(f'Error creating customer profile: {e}')
    else:
        print('Third test user already exists!')

if __name__ == '__main__':
    create_additional_test_users()