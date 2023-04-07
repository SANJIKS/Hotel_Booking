from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import force_authenticate
from rest_framework import status
from hotels.models import Booking, Favorite, Hotel, HotelRating, Like, Review, Room
from hotels.serializers import BookingSerializer, RoomSerializer
from hotels.views import BookingListAPIView, HotelViewSet, TopHotelsAPIView
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from django.urls import reverse
from datetime import datetime, timedelta

User = get_user_model()

class HotelViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = HotelViewSet.as_view({'get': 'list', 'post': 'create'})
        self.user = User.objects.create_user(
            email='example@user.com',
            password='12345'
        )
        self.hotel_data = {
            'name': 'Test hotel',
            'stars': 4,
            'address': 'Test address',
            'description': 'Test description'
        }


    def test_list_hotels(self):
        request = self.factory.get('/hotels/')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_hotel(self):
        request = self.factory.post('/hotels/', self.hotel_data)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class TopHotelsAPIViewTestCase(TestCase):
    def setUp(self):
        self.view = TopHotelsAPIView.as_view()
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create(email='user1@.com', password='1234')
        self.user2 = User.objects.create(email='user2@.com', password='1234')
        self.user3 = User.objects.create(email='user3@.com', password='1234')
        self.user4 = User.objects.create(email='user4@.com', password='1234')
        self.user5 = User.objects.create(email='user5@.com', password='1234')
        self.user6 = User.objects.create(email='user6@.com', password='1234')
        self.user7 = User.objects.create(email='user7@.com', password='1234')
        self.user8 = User.objects.create(email='user8@.com', password='1234')
        self.user9 = User.objects.create(email='user9@.com', password='1234')

        self.hotel_data = [
            {'name': 'Hotel A', 'description': 'Hotel A description', 'owner': self.user1},
            {'name': 'Hotel B', 'description': 'Hotel B description', 'owner': self.user2},
            {'name': 'Hotel C', 'description': 'Hotel C description', 'owner': self.user1},
            {'name': 'Hotel D', 'description': 'Hotel D description', 'owner': self.user1},
            {'name': 'Hotel E', 'description': 'Hotel E description', 'owner': self.user2},
            {'name': 'Hotel F', 'description': 'Hotel F description', 'owner': self.user1},
            {'name': 'Hotel G', 'description': 'Hotel G description', 'owner': self.user2},
        ]
        self.hotels = [
            Hotel.objects.create(**data)
            for data in self.hotel_data
        ]
        self.room_data = [
            {'hotel': self.hotels[0], 'room_number': '101', 'capacity': 2, 'price_per_night': 100},
            {'hotel': self.hotels[0], 'room_number': '102', 'capacity': 3, 'price_per_night': 150},
            {'hotel': self.hotels[1], 'room_number': '201', 'capacity': 2, 'price_per_night': 120},
            {'hotel': self.hotels[1], 'room_number': '202', 'capacity': 4, 'price_per_night': 180},
            {'hotel': self.hotels[2], 'room_number': '301', 'capacity': 2, 'price_per_night': 90},
            {'hotel': self.hotels[2], 'room_number': '302', 'capacity': 3, 'price_per_night': 130},
            {'hotel': self.hotels[3], 'room_number': '401', 'capacity': 2, 'price_per_night': 110},
            {'hotel': self.hotels[4], 'room_number': '501', 'capacity': 3, 'price_per_night': 140},
        ]
        self.rooms = [
            Room.objects.create(**data)
            for data in self.room_data
        ]

        self.bookings_data = [
            {'user': self.user1, 'room': self.hotels[0].rooms.first(), 'check_in': '2023-05-01', 'check_out': '2023-05-05', 'guests': 2, 'total_cost': 200.00},
            {'user': self.user1, 'room': self.hotels[0].rooms.first(), 'check_in': '2023-06-01', 'check_out': '2023-06-05', 'guests': 1, 'total_cost': 100.00},
            {'user': self.user1, 'room': self.hotels[0].rooms.first(), 'check_in': '2023-07-01', 'check_out': '2023-07-05', 'guests': 3, 'total_cost': 300.00},
            {'user': self.user2, 'room': self.hotels[1].rooms.first(), 'check_in': '2023-05-01', 'check_out': '2023-05-05', 'guests': 2, 'total_cost': 250.00},
            {'user': self.user2, 'room': self.hotels[1].rooms.first(), 'check_in': '2023-06-01', 'check_out': '2023-06-05', 'guests': 1, 'total_cost': 150.00},
            {'user': self.user1, 'room': self.hotels[2].rooms.first(), 'check_in': '2023-05-01', 'check_out': '2023-05-05', 'guests': 3, 'total_cost': 350.00},
            {'user': self.user1, 'room': self.hotels[2].rooms.first(), 'check_in': '2023-06-01', 'check_out': '2023-06-05', 'guests': 2, 'total_cost': 200.00},
            {'user': self.user1, 'room': self.hotels[3].rooms.first(), 'check_in': '2023-06-01', 'check_out': '2023-06-05', 'guests': 3, 'total_cost': 300.00}
        ]

        for data in self.bookings_data:
            Booking.objects.create(**data)

        self.ratings_data = [
            {'hotel': self.hotels[0], 'rate': 4, 'user': self.user1},
            {'hotel': self.hotels[0], 'rate': 3, 'user': self.user2},
            {'hotel': self.hotels[0], 'rate': 2, 'user': self.user3},
            {'hotel': self.hotels[1], 'rate': 5, 'user': self.user4},
            {'hotel': self.hotels[1], 'rate': 3, 'user': self.user5},
            {'hotel': self.hotels[2], 'rate': 4, 'user': self.user6},
            {'hotel': self.hotels[2], 'rate': 2, 'user': self.user7},
            {'hotel': self.hotels[3], 'rate': 5, 'user': self.user8},
            {'hotel': self.hotels[4], 'rate': 3, 'user': self.user9},
        ]
        for data in self.ratings_data:
            HotelRating.objects.create(**data)

    def test_top_hotels(self):
        request = self.factory.get('/hotels/top/')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RoomViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@gmail.com', password='12345')
        self.hotel = Hotel.objects.create(name='Test hotel', owner=self.user)
        self.room = Room.objects.create(hotel=self.hotel, room_number='101', room_type='single', capacity=1, price_per_night=100)
    
    
    def test_create_room(self):
        data = {
            'hotel': self.hotel.id,
            'room_number': '102',
            'room_type': 'Deluxe',
            'capacity': 2,
            'price_per_night': 150,
        }
        self.client.force_authenticate(user=self.user) 
        response = self.client.post('/room/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 2)
        self.assertEqual(Room.objects.last().room_number, '102')

    


    def test_get_room_detail(self):
        response = self.client.get(f'/room/{self.room.id}/')
        room = Room.objects.get(id=self.room.id)
        serializer = RoomSerializer(room)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)




class BookingCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', password='testpassword', is_owner=True)
        self.hotel = Hotel.objects.create(name='Test Hotel', address='Test Address', owner=self.user)
        self.room = Room.objects.create(hotel=self.hotel, room_number='101', room_type='Deluxe', capacity=3, price_per_night=100)

    def test_create_booking(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('booking-create', kwargs={'room_id': self.room.id})
        data = {
            'check_in': datetime.now().strftime('%Y-%m-%d'),
            'check_out': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            'guests': 2,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.get()
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.check_in, datetime.now().date())
        self.assertEqual(booking.check_out, (datetime.now() + timedelta(days=3)).date())
        self.assertEqual(booking.guests, 2)
        self.assertEqual(booking.total_cost, 300)




# class BookingListAPIViewTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.view = BookingListAPIView.as_view()
#         self.user = User.objects.create_user(
#             email='example@user.com',
#             password='12345'
#         )
#         self.hotel = Hotel.objects.create(name='Test Hotel', address='Test Address', owner=self.user)        
#         self.room = Room.objects.create(hotel=self.hotel, room_number='101', room_type='Deluxe', capacity=3, price_per_night=100)
#         self.booking = Booking.objects.create(
#             user=self.user,
#             room=self.room,
#             check_in='2023-04-10',
#             check_out='2023-04-12',
#             guests = 3,
#             total_cost = self.room.price_per_night * 3
#         )

#     def test_get_booking_list(self):
#         url = reverse('booking-history')
#         request = self.factory.get(url)
#         force_authenticate(request, user=self.user)
#         response = self.view(request)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, BookingSerializer([self.booking], many=True).data)