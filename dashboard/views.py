from hotel.models import *
from accounts.models import *
from django.utils import timezone
from django.http import HttpResponse , HttpResponseRedirect 
from django.urls import reverse 
from django.contrib.auth.decorators import login_required , permission_required
from django.shortcuts import render , get_object_or_404


def index(request):
    return render(request , 'dashboard/base.html')