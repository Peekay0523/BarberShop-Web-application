"""barbershop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from barberapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('register-submit/', views.register, name='register'),
    path('login-submit/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('reviews/', views.reviews_page, name='reviews_page'),
    path('admin-login/', views.admin_login_page, name='admin_login_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('updated-reviews/', views.updated_reviews, name='updated_reviews'),
    path('error-login/', views.error_login, name='error_login'),
    path('user-list/', views.user_list, name='user_list'),
    path('admin-login-submit/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('book-service/', views.book_service, name='book_service'),
    path('book-service/<int:service_id>/', views.book_service, name='book_service_with_id'),
    path('add-review/', views.add_review, name='add_review'),
    path('add-user-review/', views.add_user_review, name='add_user_review'),
    path('delete-client/', views.delete_client, name='delete_client'),
    path('services/', views.service_list, name='service_list'),
    path('add-service/', views.add_service, name='add_service'),
    path('edit-service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('delete-service/', views.delete_service, name='delete_service'),
    path('barbers/', views.barber_list, name='barber_list'),
    path('add-barber/', views.add_barber, name='add_barber'),
    path('edit-barber/<int:barber_id>/', views.edit_barber, name='edit_barber'),
    path('delete-barber/', views.delete_barber, name='delete_barber'),
    path('appointment-calendar/', views.appointment_calendar, name='appointment_calendar'),
    path('appointment-history/', views.appointment_history, name='appointment_history'),
    path('barber-schedule/', views.barber_schedule, name='barber_schedule'),
    path('add-barber-schedule/', views.add_barber_schedule, name='add_barber_schedule'),
    path('delete-barber-schedule/', views.delete_barber_schedule, name='delete_barber_schedule'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)