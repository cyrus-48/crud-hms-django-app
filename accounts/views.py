from django.shortcuts import render 
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView

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
        return HttpResponseRedirect(reverse(''))
    return render(request, 'auth/registration.html') 
        
    
    
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(''))
        else:
            return render(request, 'auth/login.html', {'message': 'Invalid Credentials'})
    return render(request, '')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
