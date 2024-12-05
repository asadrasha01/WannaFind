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
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

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


"""
class MessageSerializer(serializers.ModelSerializer):
    sender = UserRegistrationSerializer(read_only=True)
    receiver = UserRegistrationSerializer(read_only=True)
    item_title = serializers.CharField(source='item.title', read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'content', 'timestamp', 'is_accepted', 'is_read')
        read_only_fields = ['timestamp', 'is_read']
"""

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'item_title', 'content', 'timestamp', 'is_read']
