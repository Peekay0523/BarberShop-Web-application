from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"Customer {self.user.username}"

class Barber(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, blank=True, null=True)
    experience = models.IntegerField(help_text="Years of experience", default=0)
    photo = models.ImageField(upload_to='barbers/', blank=True, null=True)
    
    def __str__(self):
        return f"Barber {self.name}"

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('haircut', 'Haircut'),
        ('shave', 'Shave'),
        ('beard', 'Beard Treatment'),
        ('color', 'Hair Color'),
        ('treatment', 'Hair Treatment'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in minutes")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='haircut')
    
    def __str__(self):
        return f"{self.name} - R{self.price}"

class Client(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    haircut = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(default=datetime.now)
    appointment_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.name} {self.surname}"

class BankInformation(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='bank_info')
    account_number = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Bank info for {self.client.name}"

class Comment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return f"Comment by {self.client.name}"

class Review(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    sent_review = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return f"Review by {self.name}"

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"Admin {self.user.username}"

class BarberSchedule(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    def __str__(self):
        return f"{self.barber.name} - {self.day_of_week} ({self.start_time}-{self.end_time})"