from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemSerializer

# Example API view using DRF's generic views
class ItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# Custom API view example
class CustomAPI(APIView):
    def get(self, request):
        data = {"message": "Hello from the backend!"}
        return Response(data)