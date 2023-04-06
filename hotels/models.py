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



class HotelRating(models.Model):
    RATES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotel_ratings')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='ratings')
    rate = models.PositiveSmallIntegerField(choices=RATES)

    def __str__(self):
        return str(self.rate)

    class Meta:
        verbose_name = 'Рейтинг отеля'
        verbose_name_plural = 'Рейтинги отелей'
        unique_together = ['user', 'hotel']


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user', 'hotel')

    
    def __str__(self):
        return f'Liked by {self.user.email}'
    

    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ('user', 'hotel')

    def __str__(self):
        return f'{self.hotel.name} Added to favorites by {self.user.email}'
    

class Review(models.Model):
    hotel =  models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
    
    def __str__(self) -> str:
        return f'Отзыв от {self.user.email}'
    

