from django.urls import path 
from .views import *

app_name = 'hotel'
urlpatterns = [
     path('', home, name='home'),  
     path('category/<int:category_id>/', category, name='category'),
     path('categories/' , all_categories , name='all_categories'),
     path('book/',booking , name='book'),
     path('checkout/<int:booking_id>/', checkout, name='checkout'),
    path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
]