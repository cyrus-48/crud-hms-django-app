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
    
    #bookings 
    path('manage-bookings/' , views.manage_bookings , name='manage-bookings'),
    path('ajax-bookings-fetch/' , views.ajax_bookings_fetch , name='ajax-bookings-fetch'),
    path('booking/<int:booking_id>' , views.booking_detail , name='booking-detail'),
    path('edit-booking/<int:booking_id>' , views.edit_booking , name='edit-booking'),
    path('check-out/<int:booking_id>' , views.check_out , name='check-out'),
    path('booking/',views.booking , name='booking'),
    path('add-booking/',views.add_booking , name='add-booking'),
    path('fetch-available-rooms/' , views.fetch_available_rooms , name='fetch-available-rooms'),
    
    #manage users
    path('manage-users/' , views.manage_users , name='manage-users'),
    path('ajax-users-fetch/' , views.ajax_users_fetch , name='ajax-users-fetch'),
    path('user/<int:user_id>' , views.user_detail , name='user-detail'),
    path('edit-user/' , views.edit_user , name='edit-user'),
               
]