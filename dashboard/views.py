from hotel.models import *
from accounts.models import *
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize



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

# manage  rooms view
@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def manage_categories(request):
    categories = RoomCategory.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'dashboard/hotel/manage_categories.html', context)

def ajax_categories_fetch(request):
    categories = RoomCategory.objects.all()
    data = []

    for category in categories:
        data.append({
            'id': category.id,
            'name': category.name,
            'image': category.image.url, 
            'cost': category.cost,
            'date': category.added_on.strftime('%b %d, %Y'),
            'rooms': category.rooms,
            'beds': category.beds,
            'capacity': category.capacity,
            
        })

    return JsonResponse({'data': data})

def category_detail(request, category_id):
    category = get_object_or_404(RoomCategory, pk=category_id)
    context = {
        'category': category,
    }
    return render(request, 'dashboard/hotel/edit_category.html', context)


def edit_category(request ):
   if request.method == 'POST':
       category_id = request.POST['category_id']
       try: 
            category = RoomCategory.objects.get(id=category_id)
            category.name = request.POST['name']
            category.cost = request.POST['cost']
            category.beds = request.POST['beds']
            category.rooms = request.POST['rooms']
            category.capacity = request.POST['capacity']
            category.description = request.POST['description']
            if 'new_image' in request.FILES:
                 category.image = request.FILES['new_image']
            
            category.save()
            success_message = 'Category updated successfully'
            return HttpResponseRedirect(reverse('dashboard:category-detail', args=(category.id,)) + f'?success_message={success_message}')
        

       except Exception as e:
            error_message = 'Error occurred while updating category'
            return HttpResponseRedirect(reverse('dashboard:category-detail', args=(category.id,)) + f'?error_message={error_message}')
          
   else:
        error_message = 'Invalid request'
        return HttpResponseRedirect(reverse('dashboard:category-detail', args=(category.id,)) + f'?error_message={error_message}')
    
    
@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def category_delete(request):
    if request.method == 'POST':
        category_id = request.POST['category_id']
        try:
            category = RoomCategory.objects.get(id=category_id)
            category.delete()
            success_message = 'Category deleted successfully'
            return HttpResponseRedirect(reverse('dashboard:manage-categories') + f'?success_message={success_message}')
        except Exception as e:
            error_message = 'Error occurred while deleting category'
            return HttpResponseRedirect(reverse('dashboard:manage-categories') + f'?error_message={error_message}')
    else:
        error_message = 'Invalid request'
        return HttpResponseRedirect(reverse('dashboard:manage-categories') + f'?error_message={error_message}')
    
    
@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def category(request):
    return render(request, 'dashboard/hotel/add_category.html')

@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        cost = request.POST['cost']
        beds = request.POST['beds']
        rooms = request.POST['rooms']
        capacity = request.POST['capacity']
        description = request.POST['description']
        image = request.FILES['image'] if 'image' in request.FILES else None
        
        try:
            category = RoomCategory.objects.create(name=name, cost=cost, beds=beds, rooms=rooms, capacity=capacity, description=description, image=image)
            success_message = 'Category added successfully'
            return HttpResponseRedirect(reverse('dashboard:category-detail', args=(category.id,)) + f'?success_message={success_message}')
        except Exception as e:
            error_message = 'Error occurred while adding category'
            return HttpResponseRedirect(reverse('dashboard:category') + f'?error_message={error_message}')
    else:
        error_message = 'Invalid request'
        return HttpResponseRedirect(reverse('dashboard:category') + f'?error_message={error_message}')
            
@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def  manage_hotel(request):
    hotel = Hotel.objects.all()[0]
    context = {
        'hotel': hotel,
    }
    return render(request, 'dashboard/hotel/manage_hotel.html', context)


@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def update_hotel(request):
    if request.method == 'POST':
        hotel_id = request.POST['hotel_id']
        try:
            hotel = Hotel.objects.get(id=hotel_id)
            hotel.name = request.POST['name']
            hotel.email = request.POST['email']
            hotel.phone = request.POST['phone']
            hotel.address = request.POST['address']
            hotel.description = request.POST['description'] 
            hotel.save()
            success_message = 'Hotel details  updated successfully'
            return HttpResponseRedirect(reverse('dashboard:manage-hotel') + f'?success_message={success_message}')
        except Hotel.DoesNotExist:
            error_message = 'HOtel does not exist'
            return HttpResponseRedirect(reverse('dashboard:manage-hotel') + f'?error_message={error_message}')
        
        except Exception as e:
            error_message = 'Error occurred while updating hotel details '
            return HttpResponseRedirect(reverse('dashboard:manage-hotel') + f'?error_message={error_message}')
    else:
        error_message = 'Invalid request'
        return HttpResponseRedirect(reverse('dashboard:manage-hotel') + f'?error_message={error_message}') 
    
    
'''
-----------------------ROOM VIEWS-----------------------
'''
@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def ajax_rooms_fetch(request):
    rooms  = Room.objects.all()
    data = []
    print(rooms)
    
    for r in rooms:
        data.append({
            'id': r.id,
            'name': r.name,
            'category': r.category.name,
            'status': r.status,
            'date': r.added_on.strftime('%b %d, %Y'),
        })
    return JsonResponse({'data': data})
@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')      
def manage_rooms(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
    }
    return render(request, 'dashboard/hotel/manage_rooms.html', context)


#-------room detail 
@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def room_detail(request , room_id):
     try:
         room = Room.objects.get(id=room_id)
         status_choices = ['available' , 'booked' , 'not available']
         categeories = RoomCategory.objects.all()
         context = {
                'room': room,
                'status_choices': status_choices,
                'categories': categeories,
         }
         return render(request, 'dashboard/hotel/edit_room.html', context)
     
     except Room.DoesNotExist:
            error_message = 'Room does not exist'
            return HttpResponseRedirect(reverse('dashboard:manage-rooms') + f'?error_message={error_message}')
    
    
@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def edit_room(request):
    if request.method == 'POST':
        room_id = request.POST['room_id']
        try:
            room = Room.objects.get(id=room_id)
            room.name = request.POST['name']
            room.category_id = request.POST['category']
            room.status = request.POST['status']
            room.save()
            success_message = 'Room details updated successfully'
            return HttpResponseRedirect(reverse('dashboard:room-detail', args=(room.id,)) + f'?success_message={success_message}')
        except Room.DoesNotExist:
            error_message = 'Room does not exist'
            return HttpResponseRedirect(reverse('dashboard:room-detail', args=(room.id,)) + f'?error_message={error_message}')
        
        except Exception as e:
            error_message = 'Error occurred while updating room details '
            return HttpResponseRedirect(reverse('dashboard:room-detail', args=(room.id,)) + f'?error_message={error_message}')
    else:
        error_message = 'Invalid request'
        return HttpResponseRedirect(reverse('dashboard:room-detail', args=(room.id,)) + f'?error_message={error_message}')
    
    
@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def delete_room(request):
    if request.method == 'POST':
        room_id = request.POST['room_id']
        try:
            room = Room.objects.get(id=room_id)
            room.delete()
            success_message = 'Room deleted successfully'
            return HttpResponseRedirect(reverse('dashboard:manage-rooms') + f'?success_message={success_message}')
        except Exception as e:
            error_message = 'Error occurred while deleting room'
            return HttpResponseRedirect(reverse('dashboard:manage-rooms') + f'?error_message={error_message}')
    else:
        error_message = 'Invalid request'
        return HttpResponseRedirect(reverse('dashboard:manage-rooms') + f'?error_message={error_message}')
         
@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def room(request):
    categories = RoomCategory.objects.all()
    room = Room 
    context = {
        'categories': categories,
        'room': room,
    }
    return render(request, 'dashboard/hotel/add_room.html', context)    
@login_required(login_url='accounts:login')
@staff_member_required(login_url='accounts:login')
def add_room(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        status = request.POST['status']
        try:
            room = Room.objects.create(name=name, category_id=category, status=status)
            success_message = 'Room added successfully'
            return HttpResponseRedirect(reverse('dashboard:room-detail', args=(room.id,)) + f'?success_message={success_message}')
        except Exception as e:
            error_message = 'Error occurred while adding room'
            return HttpResponseRedirect(reverse('dashboard:manage-rooms') + f'?error_message={error_message}')
    else:
        error_message = 'Invalid request'
        return HttpResponseRedirect(reverse('dashboard:manage-rooms') + f'?error_message={error_message}')
    
