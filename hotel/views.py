from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import * 
from django.views.generic import ListView , DetailView  , CreateView , UpdateView , DeleteView
from django.db.models import Sum , Avg
from django.utils import timezone
from dateutil.parser import parse
from .email_service import EmailService
import requests 
from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPassword, MpesaC2bCredential

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
    user = request.user 

    if request.method == 'POST':
        room_id = request.POST['room']
        room = Room.objects.get(name=room_id)
        check_in = parse(request.POST['check_in'])
        check_out = parse(request.POST['check_out'])
        persons = request.POST['persons']

        if room.status != 'available':
            return HttpResponse('Room is not available')
        print(f"Check-in: {check_in}, Check-out: {check_out}")
        print(f"Existing Bookings: {Booking.objects.filter(room=room)}")
 
        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            user=user,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()

        if overlapping_bookings:
            error_message = 'you already have a booking  in the given time period'
            return HttpResponseRedirect(reverse('hotel:category', args=(room.category.id,)) + f'?error_message={error_message}')


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
        booking.status = "active"
        booking.save()

        # update room status
        room.status = 'booked'
        room.save()
        subject = 'Booking Confirmation'
        template = 'email/booking_confirmation_email.html'
        context = {'user': user, 'booking': booking}
        to = 'cyrusmwendwa370@gmail.com'
        

        EmailService.send_confirm_email(user, subject, template, to, context)
        success_message = 'Booking created successfully'

        return HttpResponseRedirect(reverse('hotel:category', args=(room.category.id,) ) + f'?success_message={success_message}')

    else:
        return HttpResponse('Invalid request')
    
    
@login_required(login_url='accounts:login')
def  checkout(request , booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.check_out = timezone.now()
    user = request.user
    room = booking.room
    room.status = 'available'
    booking.status = 'checked out'  
    booking.save()
    room.save()
    subject = 'Check Out Confirmation'
    template = 'email/checkout_confirmation_email.html'
    context = {'user': user, 'booking': booking}
    to = 'cyrusmwendwa370@gmail.com'

    EmailService.send_confirm_email(user, subject, template, to, context)
    success_message = 'Checked out successfully'
    
    return HttpResponseRedirect(reverse('accounts:my_bookings' )+ f'?success_message={success_message}') 
@login_required(login_url='accounts:login')
def  cancel_booking(request , booking_id):
    booking = Booking.objects.get(id=booking_id)
    user = request.user
    if booking.check_in < timezone.now():
         error_message = 'You cannot cancel a booking that has already started, please check out instead'
         return HttpResponseRedirect(reverse('accounts:my_bookings' ) + f'?error_message={error_message}')
    
    room = booking.room
    room.status = 'available'
    room.save()
    booking.status = 'cancelled'
    booking.save() 
    subject = 'Check Out Confirmation'
    template = 'email/cancellation_confirmation_email.html'
    context = {'user': user, 'booking': booking}
    to = 'cyrusmwendwa370@gmail.com'

    EmailService.send_confirm_email(user, subject, template, to, context)
    
    success_message = 'Booking cancelled successfully' 
    return HttpResponseRedirect(reverse('accounts:my_bookings' ) + f'?success_message={success_message}')

#reviews 
def reviews(request):
    all_categories  = RoomCategory.objects.all()
    context ={
        "categories":all_categories
    }
    return  render(request , 'public/reviews.html' , context)

def review_details(request , id):
    try:
        category = RoomCategory.objects.get(id=id) 
        reviews =  Review.objects.filter(category=id)
        context = {
            "category":category,
            "reviews": reviews
            
        }
        return render(request , 'public/review_details.html' , context)
        
        
    except:
        error_message = "Category does not exists"
        return HttpResponseRedirect(reverse("hotel:reviews")+f'?error_message={error_message}')
            
    
    

# payment views  
@login_required(login_url='accounts:login')
def payment(request):
    return render(request, 'public/payment_page.html')



@login_required(login_url='accounts:login')
def sendMoney(request):
    amount = 1

    if request.method == "POST":
        phone = request.POST.get('phone')

        if phone == '':
            messages.error(request,
                           "Invalid phone number. Enter a valid Safaricom number starting with 254 (e.g., 2547xxxxxxxx).")
        else:
            access_token = MpesaAccessToken.validated_mpesa_access_token
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": "Bearer %s" % access_token}

            payload = {
                "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
                "Password": LipanaMpesaPassword.decode_password,
                "Timestamp": LipanaMpesaPassword.lipa_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone,
                "PartyB": LipanaMpesaPassword.Business_short_code,
                "PhoneNumber": phone,
                "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
                "AccountReference": "mwendwa",
                "TransactionDesc": "test",
            }

            response = requests.post(api_url, json=payload, headers=headers)

            mpesa_response = response.json()
            print(mpesa_response)

            if mpesa_response['ResponseCode'] == '0':
                mpesa_transactions = MpesaTransactions.objects.create(
                    phone_number=phone, amount=amount, description='test',
                    reference=mpesa_response['CheckoutRequestID'])
                mpesa_transactions.save()

            return redirect('hotel:payment')

    # If it's not a POST request, return the form template with the initial context
    context = {'amount': amount}
    return render(request, 'public/payment_page.html', context)





