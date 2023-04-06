from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Hotel, Room, Booking, HotelRating, Like, Favorite, Review])