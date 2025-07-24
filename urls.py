"""career_guide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from application import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    
    path("add-hotel/",views.add_hotel, name="add_hotel"),
    path("hotels/",views.hotel_list, name="hotel_list"),
    path("add-room/",views.add_room, name="add_room"),
    path("room-list/",views.room_list, name="room_list"),
    path("hotel/<int:hotel_id>/rooms/", views.Room_list, name="room_list"),
    path("room/<int:room_id>/booked-dates/",views.get_booked_dates, name="get_booked_dates"),
    path("book-room/<int:pk>/",views.book_room, name="book_room"),
    path("booking-history/",views.booking_history, name="booking_history"),
    path("cancel-booking/<int:booking_id>/",views.cancel_booking, name="cancel_booking"),
    path("confirm-booking/<int:booking_id>/",views.confirm_booking, name="confirm_booking"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
