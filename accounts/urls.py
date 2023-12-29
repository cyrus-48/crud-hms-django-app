from django.urls import path 
from .views import *


app_name = 'accounts'
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/' , profile , name='profile'),
    path('profile_details/' , profile_details , name='profile_details'),
    path('edit_profile/' , edit_profile , name='edit_profile'),
    path('my_bookings/' , my_booking , name='my_bookings'),
    path('change_password/' , change_password_view , name='change_password'),
    path('edit_password/' , change_password , name='edit_password'),
]