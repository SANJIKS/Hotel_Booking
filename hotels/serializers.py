from rest_framework import serializers

from hotels.models import Booking, Hotel, Room


class HotelListSerializer(serializers.ListSerializer):
    class Meta:
        model = Hotel
        fields = ('id', 'name', 'stars', 'address', 'description', 'image')


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ['owner', 'id']
        list_serializer_class = HotelListSerializer

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    



class RoomListSerializer(serializers.ListSerializer):
    class Meta:
        model = Room
        fields = ('id', 'room_number', 'room_type', 'capacity', 'price_per_night', 'status')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('hotel', 'id', 'room_number', 'room_type', 'capacity', 'price_per_night', 'status')
        read_only_fields = ['id', 'status']
        list_serializer_class = RoomListSerializer

    def validate_hotel(self, value):
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError("Нельзя создать комнату в чужом отеле")
        return value




class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'user', 'check_in', 'check_out', 'guests', 'room')
        read_only_fields = ['id', 'user', 'room']

    