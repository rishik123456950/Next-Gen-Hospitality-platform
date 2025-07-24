from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    state=models.TextField(null=True)
    mandal=models.TextField(null=True)
    distric=models.TextField(null=True)
    image=models.ImageField(upload_to='media/hotels/')
    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    room_plan=models.ImageField(upload_to='media/plan/')
    room_type = models.CharField(max_length=50, choices=[('Single', 'Single'), ('Double', 'Double'), ('Suite', 'Suite')])
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_number}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    def __str__(self):
        return self.user.username
    
class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'),('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Confirmed')
    booking_date = models.DateTimeField(auto_now_add=True)
    cancel_by=models.TextField(null=True,blank=True)
    def __str__(self):
        return f"Booking {self.id} - {self.customer.user.username}"

