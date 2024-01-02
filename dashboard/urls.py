from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [ 
    path('' , views.index , name='dashboard-index'),
    path('manage-categories' , views.manage_categories , name='manage-categories'),
    path('ajax-categories-fetch' , views.ajax_categories_fetch , name='ajax-categories-fetch'),
    path('category/<int:category_id>' , views.category_detail , name='category-detail'),
    path('edit-category/' , views.edit_category , name='edit-category'),
               
]