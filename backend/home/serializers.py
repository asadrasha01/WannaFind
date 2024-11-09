from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ItemRequest, Message

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
    user = UserRegistrationSerializer(read_only=True)  # To include user info in ItemRequest

    class Meta:
        model = ItemRequest
        fields = ('id', 'title', 'description', 'user', 'created_at')  # Add any other fields as necessary

class MessageSerializer(serializers.ModelSerializer):
    sender = UserRegistrationSerializer(read_only=True)
    receiver = UserRegistrationSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'content', 'timestamp', 'is_accepted', 'is_read')
