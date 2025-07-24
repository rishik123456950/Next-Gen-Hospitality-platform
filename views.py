from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login ,logout,authenticate
from django.shortcuts import get_object_or_404
from .models import Hotel, Room, Booking, Customer
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Add a new hotel

# Create your views here.
def home(request):
    return render(request,'Home.html')
def register(request):
    if request.method == 'POST':
        first_name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['cnfm_password']
        phone = request.POST['phone']
        address = request.POST['address']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists, please choose a different one.')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists, please choose a different one.')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name
                )
                user.save()

                # Create Customer profile
                customer = Customer.objects.create(user=user, phone=phone, address=address)
                customer.save()

                messages.success(request, "Registration successful! Please log in.")
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            user=User.objects.get(username=username)
            if user.check_password(password):
                user = authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    messages.success(request,'login successfull')
                    return redirect('/')
                else:
                   messages.error(request,'please check the Password Properly')
                   return redirect('login')
            else:
                messages.error(request,"please check the Password Properly")  
                return redirect('login') 
        else:
            messages.error(request,"username doesn't exist")
            return redirect('login')
    return render(request,'login.html')
# Load and preprocess the dataset
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def add_hotel(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        state=request.POST.get('state')
        mandal=request.POST.get('mandal')
        distric=request.POST.get('distric')
        image = request.FILES.get("image") 
        Hotel.objects.create(User=request.user,state=state,mandal=mandal,distric=distric,name=name, location=location,image=image)
        return redirect("hotel_list")

    return render(request, "addhotel.html")
@login_required
def hotel_list(request):
    user=request.user
    if user.is_staff and user.is_superuser:
        hotels = Hotel.objects.filter(User=request.user)
        return render(request, "hotel_list.html", {"hotels": hotels})
    else:
        hotels = Hotel.objects.all()
        return render(request, "hotellist.html", {"hotels": hotels})
# View available hotels
def view_hotels(request):
    hotels = Hotel.objects.all()
    return render(request, 'view_hotels.html', {'hotels': hotels})
def add_room(request):
    if request.method == "POST":
        room_number = request.POST.get("room_number")
        room_plan = request.FILES.get("room_plan")
        room_type = request.POST.get("room_type")
        price= request.POST.get("price_per_night")

        hotel = Hotel.objects.get(User=request.user)

        Room.objects.create(
            hotel=hotel,
            room_number=room_number,
            room_plan=room_plan,
            room_type=room_type,
            price=price,
        )
        return redirect("room_list")

    hotels = Hotel.objects.all()
    return render(request, "addroom.html", {"hotels": hotels})

def room_list(request):
    rooms = Room.objects.all()
    return render(request, "room_list.html", {"rooms": rooms})

def Room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)
    return render(request, "roomlist.html", {"rooms": rooms, "hotel": hotel})
from django.http import JsonResponse
def get_booked_dates(request, room_id):
    bookings = Booking.objects.filter(room_id=room_id,status='Pending').values("check_in", "check_out")
    return JsonResponse(list(bookings), safe=False)
from datetime import datetime
def book_room(request, pk):
    room = get_object_or_404(Room, id=pk)

    if request.method == "POST":
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        customer = request.user.customer  # Assuming a Customer profile linked to User

        # Calculate total price based on nights booked
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
        nights = (check_out_date - check_in_date).days
        total_price = nights * room.price_per_night

        # Save the booking
        Booking.objects.create(
            customer=customer,
            hotel=room.hotel,
            room=room,
            check_in=check_in_date,
            check_out=check_out_date,
            total_price=total_price,
            status="Confirmed",
        )

        return redirect("room_list", hotel_id=room.hotel.id)

    return render(request, "book_room.html", {"room": room})


@login_required
def booking_history(request):
    if hasattr(request.user, 'customer'):  # If logged in as a Customer
        bookings = Booking.objects.filter(customer=request.user.customer)
    elif Hotel.objects.filter(User=request.user).exists():  # If logged in as a Hotel Owner
        hotels = Hotel.objects.filter(User=request.user)
        bookings = Booking.objects.filter(hotel__in=hotels)
    else:
        messages.error(request, "Unauthorized access")
        return redirect("home")

    return render(request, "booking_history.html", {"bookings": bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user == booking.customer.user or request.user == booking.hotel.User:  # Ensure only owner or customer can cancel
        booking.status = "Cancelled"
        booking.cancel_by=request.user.username
        booking.save()
        messages.success(request, "Booking has been cancelled.")
        return redirect("booking_history")
    else:
        messages.error(request, "You are not authorized to cancel this booking.")
        return redirect("booking_history")
    

@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user == booking.customer.user or request.user == booking.hotel.User:  # Ensure only owner or customer can cancel
        booking.status = "Confirmed"
        booking.save()
        messages.success(request, "Booking has been confirm.")
        return redirect("booking_history")
    else:
        messages.error(request, "You are not authorized to cancel this booking.")
        return redirect("booking_history")