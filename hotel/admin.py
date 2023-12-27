from django.contrib import admin
from .models import *

admin.site.register(Hotel)
admin.site.register(RoomCategory)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Review)
