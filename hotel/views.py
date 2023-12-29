from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import * 
from django.views.generic import ListView , DetailView  , CreateView , UpdateView , DeleteView
from django.db.models import Sum

def home(request):     
    room_categories  = RoomCategory.objects.all()[:4]
    categories_count = RoomCategory.objects.all().count()
    visitors_count = Booking.objects.all().count()
    rooms_count = RoomCategory.objects.aggregate(total_rooms = Sum('rooms'))['total_rooms'] 
    reviews_count = Review.objects.all().count()

    context = {
        'room_categories': room_categories,
        'rooms_count':rooms_count,
        'visitors_count':visitors_count,
        'categories_count':categories_count,
        'reviews_count':reviews_count
    }
    
    return render(request, 'public/index.html' , context)


def category(request , category_id):
    category = RoomCategory.objects.get(id=category_id)
    description = category.description.split(',')
    available_rooms = Room.objects.filter(category=category , status='available').count()
    categories_count = RoomCategory.objects.all().count()
    visitors_count = Booking.objects.all().count()
    rooms_count = RoomCategory.objects.aggregate(total_rooms = Sum('rooms'))['total_rooms'] 
    reviews_count = Review.objects.all().count()
    
    possible_rooms_for_category  = Room.objects.filter(category=category , status='available')

    context = {
        'category': category,
        'available_rooms': available_rooms,
        'description': description,
        'rooms_count':rooms_count,
        'visitors_count':visitors_count,
        'categories_count':categories_count,
        'reviews_count':reviews_count,
        'possible_rooms_for_category':possible_rooms_for_category,
        
    }
    return render(request, 'public/category_detail.html' , context)


def all_categories(request):
    categories = RoomCategory.objects.all()
    categories_count = RoomCategory.objects.all().count()
    visitors_count = Booking.objects.all().count()
    rooms_count = RoomCategory.objects.aggregate(total_rooms = Sum('rooms'))['total_rooms'] 
    reviews_count = Review.objects.all().count()
    context = {
        'room_categories': categories,
        'rooms_count':rooms_count,
        'visitors_count':visitors_count,
        'categories_count':categories_count,
        'reviews_count':reviews_count
    }
    return render(request, 'public/all_categories.html' , context)
@login_required(login_url='accounts:login')
def booking(request):
    if request.method == 'POST':
        user = request.user
        room_id = request.POST['room']
        room = Room.objects.get(name=room_id)
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        persons = request.POST['persons'] 
        if room.status != 'available':
            return HttpResponse('Room is not available') 
        if check_in > check_out:
            return HttpResponse('Invalid dates')
         
        if int(persons) > room.category.capacity:
            return HttpResponse('Invalid number of persons') 
        # create booking
        booking = Booking.objects.create(
            room=room,
            user=user,
            check_in=check_in,
            check_out=check_out,
            persons=persons
        ) 
        booking.save()
        # update room status
        room.status = 'booked'
        room.save() 
        return HttpResponseRedirect(reverse('hotel:category' , args=(room.category.id,)))

    else:
        return HttpResponse('Invalid request')

    
 
    



