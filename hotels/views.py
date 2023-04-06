from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Avg, Count


from hotels.models import Booking, Hotel, Room
from hotels.permissions import IsOwner, IsOwnerAndAuthor, IsHisHotel
from hotels.serializers import BookingSerializer, HotelSerializer, RatingSerializer, RoomSerializer
# Create your views here.



class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['stars']
    search_fields = ['title', 'description']


    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsOwner]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsOwnerAndAuthor]
        return super().get_permissions()
    

    def get_serializer_context(self):
        """  
        Метод для добавления дополнительных данных в сериалайзеры
        """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
    

    def get_serializer_class(self):
        if self.action == 'rate_hotel':
            return RatingSerializer
        return super().get_serializer_class()
    

    @action(methods=['POST'], detail=True, url_path='rate')
    def rate_hotel(self, request, pk=None) -> Response:
        hotel = self.get_object()
        serializer = RatingSerializer(data=request.data, context={'request': request, 'hotel': hotel})
        serializer.is_valid(raise_exception=True)
        serializer.save(hotel=hotel)
        return Response(serializer.data)
    


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

        return Response({'message': 'Бронирование создано'}, status=status.HTTP_201_CREATED)





class BookingListAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user)