from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import HotelViewSet, RoomViewSet, BookingCreateAPIView, BookingListAPIView

router = DefaultRouter()
router.register('hotel', HotelViewSet, 'hotels')
router.register('room', RoomViewSet, 'rooms')

urlpatterns = [
    path('', include(router.urls)),
    path('bookings/<int:room_id>/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('bookings/', BookingListAPIView.as_view(), name='booking-history')
]