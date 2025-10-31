from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Client, Review, BankInformation, Comment, Customer, Barber, Service, BarberSchedule
from datetime import datetime
import json

def home_page(request):
    reviews = Review.objects.all().order_by('-sent_review')[:5]  # Get latest 5 reviews
    services = Service.objects.all()
    barbers = Barber.objects.all()
    return render(request, 'index.html', {'reviews': reviews, 'services': services, 'barbers': barbers})

def register_page(request):
    return render(request, 'register.html')

def login_page(request):
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST.get('phone', '')
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register_page')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register_page')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register_page')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create customer profile
        customer = Customer.objects.create(
            user=user,
            phone=phone
        )
        
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login_page')
    
    return redirect('register_page')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login_page')
    
    return redirect('login_page')

@login_required
def profile(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        customer = None
    
    # Get customer's bookings
    bookings = Client.objects.filter(name=request.user.first_name, surname=request.user.last_name)
    
    return render(request, 'profile.html', {
        'customer': customer,
        'bookings': bookings
    })

@login_required
def appointment_history(request):
    # Get customer's bookings
    bookings = Client.objects.filter(name=request.user.first_name, surname=request.user.last_name).order_by('-appointment_date')
    
    return render(request, 'appointment_history.html', {
        'bookings': bookings,
        'now': datetime.now()
    })

@login_required
def barber_schedule(request):
    barbers = Barber.objects.all()
    schedules = BarberSchedule.objects.select_related('barber').all()
    
    # Group schedules by barber
    barber_schedules = {}
    for barber in barbers:
        barber_schedules[barber.id] = {
            'barber': barber,
            'schedules': schedules.filter(barber=barber)
        }
    
    return render(request, 'barber_schedule.html', {
        'barber_schedules': barber_schedules,
        'barbers': barbers
    })

@login_required
def add_barber_schedule(request):
    if request.method == 'POST':
        barber_id = request.POST['barber']
        day_of_week = request.POST['day_of_week']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        
        try:
            barber = Barber.objects.get(id=barber_id)
            schedule = BarberSchedule(
                barber=barber,
                day_of_week=day_of_week,
                start_time=start_time,
                end_time=end_time
            )
            schedule.save()
            
            messages.success(request, 'Schedule added successfully!')
        except Barber.DoesNotExist:
            messages.error(request, 'Barber not found!')
        except Exception as e:
            messages.error(request, f'Error adding schedule: {str(e)}')
        
        return redirect('barber_schedule')
    
    barbers = Barber.objects.all()
    return render(request, 'add_barber_schedule.html', {'barbers': barbers})

@login_required
def delete_barber_schedule(request):
    if request.method == 'POST':
        schedule_id = request.POST['schedule_id']
        try:
            schedule = BarberSchedule.objects.get(id=schedule_id)
            schedule.delete()
            return JsonResponse({'success': True, 'message': 'Schedule deleted successfully!'})
        except BarberSchedule.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Schedule not found'})
    
    return JsonResponse({'success': False})

@login_required
def admin_dashboard(request):
    # Get statistics
    total_customers = Customer.objects.count()
    total_barbers = Barber.objects.count()
    total_services = Service.objects.count()
    total_appointments = Client.objects.count()
    
    # Get recent appointments
    recent_appointments = Client.objects.select_related().order_by('-created_date')[:10]
    
    # Get appointment counts by day for the last 7 days
    from django.db.models import Count
    from datetime import datetime, timedelta
    
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    appointments_by_day = Client.objects.filter(
        created_date__date__gte=week_ago
    ).extra(
        select={'day': 'date(created_date)'}
    ).values('day').annotate(count=Count('id')).order_by('day')
    
    # Prepare data for chart
    chart_data = []
    for i in range(7):
        day = week_ago + timedelta(days=i)
        count = next((item['count'] for item in appointments_by_day if str(item['day']) == str(day)), 0)
        chart_data.append({
            'date': day.strftime('%a'),
            'count': count
        })
    
    return render(request, 'admin_dashboard.html', {
        'total_customers': total_customers,
        'total_barbers': total_barbers,
        'total_services': total_services,
        'total_appointments': total_appointments,
        'recent_appointments': recent_appointments,
        'chart_data': chart_data
    })

def logout_view(request):
    logout(request)
    return redirect('home')

def reviews_page(request):
    return render(request, 'reviews.html')

def admin_login_page(request):
    return render(request, 'admin_login.html')

@login_required
def dashboard(request):
    clients = Client.objects.all().order_by('-created_date')
    return render(request, 'dashboard.html', {'clients': clients})

@login_required
def updated_reviews(request):
    reviews = Review.objects.all().order_by('-sent_review')
    return render(request, 'updated_reviews.html', {'reviews': reviews})

def error_login(request):
    return render(request, 'error_login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('error_login')
    
    return redirect('admin_login_page')

def admin_logout(request):
    logout(request)
    return redirect('home')

def book_appointment(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        haircut = request.POST['haircut']
        price = request.POST['price']
        book_date = request.POST['bookDate']
        
        # Create client
        client = Client(
            name=name,
            surname=surname,
            haircut=haircut,
            amount_paid=price,
            appointment_date=book_date
        )
        client.save()
        
        # If online payment was selected, create bank info
        if 'paymentType' in request.POST and request.POST['paymentType'] == 'online':
            bank_info = BankInformation(client=client)
            bank_info.save()
        
        # Send confirmation email
        try:
            # In a real app, you would collect the customer's email
            # For now, we'll use a placeholder
            customer_email = f'{name.lower()}.{surname.lower()}@example.com'
            
            # Render email template
            from django.template.loader import render_to_string
            email_content = render_to_string('appointment_confirmation_email.txt', {'client': client})
            
            send_mail(
                'Appointment Confirmation - Clean|CUT Barber Shop',
                email_content,
                settings.DEFAULT_FROM_EMAIL,
                [customer_email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't fail the booking
            print(f"Error sending email: {e}")
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

def add_review(request):
    if request.method == 'POST':
        name = request.POST['name']
        message = request.POST['message']
        
        review = Review(name=name, message=message)
        review.save()
        
        return redirect('updated_reviews')
    
    return redirect('reviews_page')

@login_required
def service_list(request):
    category = request.GET.get('category', '')
    
    if category:
        services = Service.objects.filter(category=category)
    else:
        services = Service.objects.all()
    
    # Get all categories for the filter dropdown
    categories = Service.CATEGORY_CHOICES
    
    return render(request, 'services.html', {
        'services': services,
        'categories': categories,
        'selected_category': category
    })

@login_required
def add_service(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        duration = request.POST['duration']
        category = request.POST['category']
        
        service = Service(
            name=name,
            description=description,
            price=price,
            duration=duration,
            category=category
        )
        service.save()
        
        messages.success(request, 'Service added successfully!')
        return redirect('service_list')
    
    return render(request, 'add_service.html')

@login_required
def delete_service(request):
    if request.method == 'POST':
        service_id = request.POST['service_id']
        try:
            service = Service.objects.get(id=service_id)
            service.delete()
            return JsonResponse({'success': True, 'message': 'Service deleted successfully!'})
        except Service.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Service not found'})
    
    return JsonResponse({'success': False})

@login_required
def barber_list(request):
    barbers = Barber.objects.all()
    return render(request, 'barbers.html', {'barbers': barbers})

@login_required
def add_barber(request):
    if request.method == 'POST':
        name = request.POST['name']
        specialty = request.POST['specialty']
        experience = request.POST['experience']
        
        barber = Barber(
            name=name,
            specialty=specialty,
            experience=experience
        )
        barber.save()
        
        messages.success(request, 'Barber added successfully!')
        return redirect('barber_list')
    
    return render(request, 'add_barber.html')

@login_required
def delete_barber(request):
    if request.method == 'POST':
        barber_id = request.POST['barber_id']
        try:
            barber = Barber.objects.get(id=barber_id)
            barber.delete()
            return JsonResponse({'success': True, 'message': 'Barber deleted successfully!'})
        except Barber.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Barber not found'})
    
    return JsonResponse({'success': False})

@login_required
def delete_client(request):
    if request.method == 'POST':
        client_id = request.POST['cus_id']
        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            return JsonResponse({'success': True, 'message': 'Customer Deleted'})
        except Client.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Customer not found'})
    
    return JsonResponse({'success': False})

@login_required
def appointment_calendar(request):
    # Get all appointments for the current month
    today = datetime.now()
    appointments = Client.objects.filter(appointment_date__month=today.month).order_by('appointment_date')
    
    # Get all services and barbers for the form
    services = Service.objects.all()
    barbers = Barber.objects.all()
    
    return render(request, 'appointment_calendar.html', {
        'appointments': appointments,
        'services': services,
        'barbers': barbers,
        'current_month': today.strftime('%B %Y')
    })