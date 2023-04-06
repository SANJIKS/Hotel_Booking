from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    image = models.ImageField(upload_to='hotel_image/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    stars = models.CharField(choices=(('1', '1 звезда'), ('2', '2 звезды'), ('3', '3 звезды'), ('4', '4 звезды'), ('5', '5 звезд')))
    bookings_count = models.PositiveIntegerField(default=0, verbose_name='количество бронирований')

    def __str__(self):
        return self.name



class Room(models.Model):
    STANDARD = 'Standard'
    DELUXE = 'Deluxe'

    ROOM_TYPE_CHOICES = [
        (STANDARD, 'Standard'),
        (DELUXE, 'Deluxe'),
    ]
    
    STATUS_CHOICES = (
        ('Loose', 'loose'),
        ('Booked', 'booked'),
    )
    

    ROOM_CAPACITY_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    )



    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    capacity = models.PositiveSmallIntegerField(choices=ROOM_CAPACITY_CHOICES)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='Loose')


    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_number}"



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveSmallIntegerField()
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.email} - {self.room.hotel.name} - Room {self.room.room_number}"