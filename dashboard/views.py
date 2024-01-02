from hotel.models import *
from accounts.models import *
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required


@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def index(request):
    number_of_rooms = Room.objects.count()
    number_of_categories = RoomCategory.objects.count()
    number_of_customers = CustomUser.objects.filter(is_staff=False).count()
    number_of_staff = CustomUser.objects.filter(is_staff=True).count()

    number_of_bookings = Booking.objects.count()
    number_of_bookings_today = Booking.objects.filter(check_in=timezone.now()).count()
    number_of_bookings_this_month = Booking.objects.filter(check_in__month=timezone.now().month).count()
    number_of_bookings_this_year = Booking.objects.filter(check_in__year=timezone.now().year).count()
    bookings = Booking.objects.all()[0:10]

    context = {
        'num_of_rooms': number_of_rooms,
        'num_of_categories': number_of_categories,
        'num_of_customers': number_of_customers,
        'num_of_staff': number_of_staff,
        'num_of_bookings': number_of_bookings,
        'number_of_bookings_today': number_of_bookings_today,
        'number_of_bookings_this_month': number_of_bookings_this_month,
        'number_of_bookings_this_year': number_of_bookings_this_year,
        'bookings': bookings,
    }

    return render(request, 'dashboard/home.html' ,  context)



