from django.shortcuts import render 
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from hotel.models import *

def register_view(request):
    if request.method  == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
         
        if password != confirm_password:
            return render(request, 'auth/registration.html', {'message': 'Password Mismatch'})
        
        #USER CREATION
        user = CustomUser.objects.create_user(email=email, password=password)
        user.first_name = fname
        user.last_name = lname
        user.gender = gender
        user.address = address
        user.save()
        
        login(request, user)
        return HttpResponseRedirect(reverse('accounts:login'))
    return render(request, 'auth/registration.html') 
        
    
    
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('hotel:home'))
        else:
            return render(request, 'auth/login.html', {'message': 'Invalid Credentials'})
    return render(request, 'auth/login.html')

@login_required(login_url='accounts:login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))

@login_required(login_url='accounts:login')
def profile(request):
    user  =  request.user
    context = {
        'user':user
    }
    return render(request , 'public/profile.html' , context)

@login_required(login_url='accounts:login')
def profile_details(request):
    user  =  request.user
    context = {
        'user':user
    }
    return render(request , 'public/edit_profile.html' , context)

@login_required(login_url='accounts:login')
def edit_profile(request):
    if request.method == 'POST':
        first_name  = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email = request.POST.get('email')
        address  = request.POST.get('address')
        gender = request.POST.ger('gender')
        user = request.user
        
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.address = address
        user.gender = gender
        user.save()
        
        return render(request , 'public/profile.html' , {'message':'Profile Updated'})
    else:
        return render(request , 'public/profile.html' , {'message':'Invalid Request'})
    
    
@login_required(login_url='accounts:login')
def my_booking(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    context = {
        'bookings':bookings
    }
    return render(request , 'public/my_bookings.html' , context)

@login_required(login_url='accounts:login')
def change_password_view(request):
    user  =  request.user
    context = {
        'user':user
    }
    return render(request,'public/change_password.html',context)
@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = request.user
        if user.check_password(old_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return render(request , 'public/profile.html' , {'message':'Password Updated'})
            else:
                return render(request , 'public/change_password.html' , {'message':'Password Mismatch'})
        else:
            return render(request , 'public/change_password.html' , {'message':'Invalid Password'})
    else:
        return render(request , 'public/change_password.html' , {'message':'Invalid Request'})
