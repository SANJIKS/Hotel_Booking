from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Avg, Count
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.cache import cache_page

from hotels.models import Booking, Favorite, Hotel, Like, Review, Room
from hotels.permissions import IsAuthor, IsOwner, IsOwnerAndAuthor, IsHisHotel
from hotels.serializers import BookingSerializer, FavoriteSerializer, HotelSerializer, LikeSerializer, RatingSerializer, ReviewSerializer, RoomSerializer
# Create your views here.



class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['stars']
    search_fields = ['title', 'description']


    def get_permissions(self):
        if self.action == 'rate_hotel' or self.action == 'like' or self.action == 'favorite' or self.action == 'review':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            self.permission_classes = [IsOwner]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsOwnerAndAuthor]
        return super().get_permissions()
        

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    

    def get_serializer_class(self):
        if self.action == 'rate_hotel':
            return RatingSerializer
        elif self.action == 'like':
            return LikeSerializer
        elif self.action == 'favorite':
            return FavoriteSerializer
        elif self.action == 'review':
            return ReviewSerializer
        return super().get_serializer_class()
    

    @action(methods=['POST', 'DELETE'], detail=True)
    def review(self, request, pk=None):
        hotel = self.get_object()
        if request.method == 'POST':
            serializer = ReviewSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, hotel=hotel)
            return Response(serializer.data)
        if request.method == 'DELETE':
            review = get_object_or_404(hotel.reviews, pk=pk)
            review.delete()
            return Response({'message': 'Ваш коммент удален'})

    

    @action(methods=['POST'], detail=True, url_path='rate')
    def rate_hotel(self, request, pk=None) -> Response:
        hotel = self.get_object()
        serializer = RatingSerializer(data=request.data, context={'request': request, 'hotel': hotel})
        serializer.is_valid(raise_exception=True)
        serializer.save(hotel=hotel)
        return Response(serializer.data)
    

    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        hotel = self.get_object()
        like = Like.objects.filter(user=request.user, hotel=hotel)
        if like.exists():
            like.delete()
            liked = False
        else:
            Like.objects.create(user=request.user, hotel=hotel)
            liked = True
        likes_count = Like.objects.filter(hotel=hotel).count()
        response_data = {'liked': liked, 'likes_count': likes_count}
        return Response(response_data)
    

    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk=None):
        hotel = self.get_object()
        favor = Favorite.objects.filter(user=request.user, hotel=hotel)
        if favor.exists():
            favor.delete()
            favor = False
        else:
            Favorite.objects.create(user=request.user, hotel=hotel)
            favor = True

        return Response({'In Favorite': favor})
    


class TopHotelsAPIView(generics.ListAPIView):
    serializer_class = HotelSerializer

    def get_queryset(self):
        return Hotel.objects.annotate(num_bookings=Count('bookings_count'), avg_rating=Avg('ratings__rate')).order_by('-num_bookings', '-avg_rating')[:5]
    
    



class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsHisHotel]
        return super().get_permissions()


    

class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        room_id = kwargs.get('room_id')
        try:
            room = Room.objects.get(id=room_id)
            hotel = room.hotel
        except Room.DoesNotExist:
            return Response({'message': 'Комната не найдена'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']
        
        if Booking.objects.filter(room=room, check_in__lte=check_out, check_out__gte=check_in).exists():
            return Response({'message': 'Комната уже забронирована на указанный период времени.'}, status=status.HTTP_400_BAD_REQUEST)

        booking = Booking(
            user=self.request.user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            guests=serializer.validated_data['guests'],
            total_cost=room.price_per_night * (check_out - check_in).days,
        )
        booking.save()
        room.status = 'Booked'
        room.save()
        hotel.bookings_count += 1 
        hotel.save()
        print(room.price_per_night * (check_out - check_in).days)

        subject = 'Ваша комната забронирована'
        message = f'Здравствуйте, вы успешно забронировали комнату {room.room_number} отеля {hotel.name}, с {check_in} по {check_out}. Сумма оплаты: {room.price_per_night * (check_out - check_in).days} сом. Спасибо что выбрали наш сервис!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email]
        send_mail(subject, message, from_email, recipient_list)

        return Response({'message': 'Бронирование создано'}, status=status.HTTP_201_CREATED)

    


class BookingListAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user)
    

class FavoriteListAPIView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)
    


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context