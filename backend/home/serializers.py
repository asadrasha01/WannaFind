from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ItemRequest, Message, Profile, Feedback
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

class FeedbackSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'reviewer', 'reviewee', 'comment', 'rating', 'created_at', 'reviewer_username']
        read_only_fields = ['reviewer']

class ProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = ['name', 'surname', 'phone_number', 'city', 'country', 'profile_image']

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    received_feedbacks = FeedbackSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'profile', 'received_feedbacks']
        read_only_fields = ['username', 'email']

    def update(self, instance, validated_data):
        # Update user fields
        profile_data = validated_data.pop('profile', {})
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update profile fields
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance

class ItemRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ItemRequest
        fields = '__all__'  # All necessary fields are included

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
    item_title = serializers.CharField(source='item.title', read_only=True)
    item = serializers.PrimaryKeyRelatedField(queryset=ItemRequest.objects.all())

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'receiver', 'item',
            'sender_username', 'receiver_username', 'item_title',
            'content', 'timestamp', 'is_read'
        ]
        read_only_fields = ['sender']

    def create(self, validated_data):
        user = self.context['request'].user
        return Message.objects.create(sender=user, **validated_data)
