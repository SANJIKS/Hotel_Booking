from rest_framework import serializers
from django.db.models import Avg

from hotels.models import Booking, Favorite, Hotel, HotelRating, Like, Review, Room


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    
    class Meta:
        model = Like
        fields = ('user',)


class HotelListSerializer(serializers.ListSerializer):
    class Meta:
        model = Hotel
        fields = ('id', 'name', 'stars', 'address', 'description', 'image')



class HotelSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(method_name='get_likes_count')
    image = serializers.ImageField(max_length=None, use_url=True)
    

    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ['owner', 'id']
        list_serializer_class = HotelListSerializer


    def get_likes_count(self, instance) -> int:
        return Like.objects.filter(hotel=instance).count()
    

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['liked_users'] = LikeSerializer(instance.likes.all(), many=True).data
        representation['rating'] = instance.ratings.aggregate(Avg('rate'))['rate__avg']
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        return representation
    



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



class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRating
        fields = ('id', 'user', 'hotel', 'rate')
        read_only_fields = ['user', 'hotel']


    def validate(self, attrs):
        user = self.context.get('request').user
        hotel = self.context.get('hotel')
        rate = HotelRating.objects.filter(user=user, hotel=hotel).exists()
        if rate:
            raise serializers.ValidationError({'message': 'Rate already exists'})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)
    

class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Favorite
        fields = ('user', 'hotel')



class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'user', 'hotel', 'text', 'created_at', 'updated_at')
        read_only_fields = ['hotel']