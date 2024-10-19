from rest_framework import serializers
from .models import ItemRequest

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemRequest
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']
