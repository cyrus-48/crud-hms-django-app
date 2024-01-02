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
            