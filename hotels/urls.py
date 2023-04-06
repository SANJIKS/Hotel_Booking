from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import HotelViewSet, RoomViewSet, BookingCreateAPIView, BookingListAPIView, TopHotelsAPIView, FavoriteListAPIView

router = DefaultRouter()
router.register('hotel', HotelViewSet, 'hotels')
router.register('room', RoomViewSet, 'rooms')

urlpatterns = [
    path('', include(router.urls)),
    path('bookings/<int:room_id>/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('bookings/', BookingListAPIView.as_view(), name='booking-history'),
    path('top-hotels/', TopHotelsAPIView.as_view(), name='top-hotels'),
    path('favorites/', FavoriteListAPIView.as_view(), name='favorites')
]