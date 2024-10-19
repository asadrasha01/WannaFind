from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ItemRequest
from .serializers import RequestSerializer

class RequestListView(APIView):
    """
    Handles GET requests for listing all requests.
    """
    def get(self, request):
        # Get all requests from the database
        requests = ItemRequest.objects.all()
        # Serialize the data
        serializer = RequestSerializer(requests, many=True)
        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)

class RequestDetailView(APIView):
    """
    Handles GET requests for retrieving a single request by its ID.
    """
    def get(self, request, pk):
        try:
            # Get a single request by its primary key (ID)
            request_obj = ItemRequest.objects.get(pk=pk)
        except ItemRequest.DoesNotExist:
            return Response({"error": "Request not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the data
        serializer = RequestSerializer(request_obj)
        # Return the serialized data as a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)
