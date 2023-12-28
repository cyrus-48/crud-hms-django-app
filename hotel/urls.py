from django.urls import path 
from .views import *

app_name = 'hotel'
urlpatterns = [
     path('home/', home, name='home'),  
     path('category/<int:category_id>/', category, name='category'),
     path('categories/' , all_categories , name='all_categories')
]