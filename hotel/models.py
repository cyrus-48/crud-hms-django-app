from django.db import models 
from django.db.models import Sum , Avg


class Hotel(models.Model):
    name  = models.CharField(max_length=255)
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
class RoomCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.IntegerField()
    beds = models.IntegerField()
    rooms = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateTimeField(auto_now_add=True) 
    image = models.ImageField(upload_to="room_category_images")
    
    def __str__(self):
        return self.name
    @property
    def total_reviews(self):
        return self.review_set.count()

    @property
    def average_rating(self):
         average  = self.review_set.aggregate(Avg('rating'))['rating__avg']
         return round(average) if average is not None else 0
     
    @property
    def available_rooms(self):
        return self.room_set.filter(status='available').count()

class Room(models.Model):
    name  = models.CharField(max_length=255 , unique=True)
    category = models.ForeignKey('RoomCategory' , on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('available' , 'available' ) , 
        ('booked' , 'booked'),
        ('not available' , 'not available')
    )
    status = models.CharField(max_length=255 , choices=STATUS_CHOICES)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class Booking(models.Model):
    room = models.ForeignKey('Room' , on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.CustomUser' , on_delete=models.CASCADE)
    persons = models.IntegerField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    STATUS_CHOICES = (
        ('active' , 'active') , 
        ('cancelled' , 'cancelled') , 
        ('checked out' , 'checked out')
    )
    status = models.CharField(max_length=255 , choices=STATUS_CHOICES , default='active')
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email
    
class Payment(models.Model):
    booking = models.ForeignKey('Booking' , on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=255)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.booking.user.email
    
class Review(models.Model):
    category = models.ForeignKey('RoomCategory' , on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.CustomUser' , on_delete=models.CASCADE) 
    RATINGS = (
        (1 , 1) , 
        (2 , 2) , 
        (3 , 3) , 
        (4 , 4) , 
        (5 , 5) , 
    ) 
    comment = models.TextField()
    rating = models.IntegerField(choices=RATINGS)
    added_on = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return self.booking.user.email
    
    
    