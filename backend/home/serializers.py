from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ItemRequest, Message
from django.conf import settings

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')  # Include fields as needed

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    # Add profile-related fields explicitly
    name = serializers.CharField(source='profile.name', required=False)
    surname = serializers.CharField(source='profile.surname', required=False)
    phone_number = serializers.CharField(source='profile.phone_number', required=False)
    city = serializers.CharField(source='profile.city', required=False)
    country = serializers.CharField(source='profile.country', required=False)
    profile_image = serializers.ImageField(source='profile.profile_image', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'surname', 'phone_number', 'city', 'country', 'profile_image']
        read_only_fields = ['username', 'email']

    def update(self, instance, validated_data):
        # Update User fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update Profile fields
        profile_data = validated_data.get('profile', {})
        profile = instance.profile
        profile.name = profile_data.get('name', profile.name)
        profile.surname = profile_data.get('surname', profile.surname)
        profile.phone_number = profile_data.get('phone_number', profile.phone_number)
        profile.city = profile_data.get('city', profile.city)
        profile.country = profile_data.get('country', profile.country)
        profile.profile_image = profile_data.get('profile_image', profile.profile_image)
        profile.save()

        return instance

class ItemRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ItemRequest
        fields = '__all__'  # Ensure all necessary fields are included

    def create(self, validated_data):
        # Attach user from the context
        user = self.context['request'].user
        validated_data['user'] = user
        return ItemRequest.objects.create(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image:
            if request:
                # Generate full URL for the image
                representation['image'] = request.build_absolute_uri(instance.image.url)
            else:
                # Fallback to relative URL if request is unavailable
                representation['image'] = settings.MEDIA_URL + instance.image.name
        return representation


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'item_title', 'content', 'timestamp', 'is_read']
