from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [ 
    path('' , views.index , name='dashboard-index'),
    path('manage-categories' , views.manage_categories , name='manage-categories'),
    path('ajax-categories-fetch' , views.ajax_categories_fetch , name='ajax-categories-fetch'),
    path('category/<int:category_id>' , views.category_detail , name='category-detail'),
    path('edit-category/' , views.edit_category , name='edit-category'),
    path('manage-hotel/' , views.manage_hotel , name='manage-hotel'),
    path('update-hotel/' , views.update_hotel , name='update-hotel'),
    path('category/', views.category, name='category'),
    path('add-category/', views.add_category, name='add-category'),
    path('delete-category/', views.category_delete, name='delete-category'),
    
    # manage rooms
    path('manage-rooms/' , views.manage_rooms , name='manage-rooms'),
    path('ajax-rooms-fetch/' , views.ajax_rooms_fetch , name='ajax-rooms-fetch'),
    path('room/<int:room_id>' , views.room_detail , name='room-detail'),
    path('edit-room/' , views.edit_room , name='edit-room'), 
    path('delete-room/' , views.delete_room , name='delete-room'),
    path('room/',views.room , name='room'),
    path('add-room/',views.add_room , name='add-room'),
               
]