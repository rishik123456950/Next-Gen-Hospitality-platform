from django.contrib import admin

# Register your models here.
from .models import Hotel,Room,Customer,Booking
admin.site.register(Hotel)
admin.site.register(Booking)