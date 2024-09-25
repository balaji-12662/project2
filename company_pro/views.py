from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .models import Item
from .serializers import ItemSerializer

# Create item
class ItemCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Read item with caching (Redis)
class ItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Try to get the item from Redis cache
        item = cache.get(f'item_{pk}')
        if not item:
            # If not in cache, fetch from DB
            item = get_object_or_404(Item, pk=pk)
            # Cache the item
            cache.set(f'item_{pk}', item, timeout=60*15)  # Cache for 15 minutes
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Update item
class ItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete item
class ItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response({'message': 'Item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
