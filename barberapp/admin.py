from django.contrib import admin
from .models import Client, BankInformation, Comment, Review, Admin, Barber, Service, Customer, BarberSchedule

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'haircut', 'amount_paid', 'appointment_date', 'created_date')
    list_filter = ('haircut', 'created_date', 'appointment_date')
    search_fields = ('name', 'surname')

@admin.register(BankInformation)
class BankInformationAdmin(admin.ModelAdmin):
    list_display = ('client', 'account_number', 'bank_name')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('client', 'text', 'created_date')
    list_filter = ('created_date',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'sent_review')
    list_filter = ('sent_review',)
    search_fields = ('name', 'message')

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')

@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'experience')
    list_filter = ('specialty',)
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration')
    list_filter = ('price',)
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(BarberSchedule)
class BarberScheduleAdmin(admin.ModelAdmin):
    list_display = ('barber', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'barber')