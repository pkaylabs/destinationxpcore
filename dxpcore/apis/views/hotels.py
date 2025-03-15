from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apis.models import Hotel
from apis.serializers import HotelSerializer


class HotelListAPI(APIView):
    '''Hotel List API endpoint'''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        '''Get all hotels. Everyone can view the hotels'''
        hotels = Hotel.objects.all().order_by('-created_at', 'name')
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''Create a new hotel. Only staff can create a hotel'''
        user = request.user
        if not user.is_staff:
            return Response({'message': 'You are not authorized to create a hotel'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = HotelSerializer(data=request.data)
        hotel_id = request.data.get('id')
        hotel = None
        if hotel_id:
            hotel = Hotel.objects.filter(id=hotel_id).first()
            if hotel:
                serializer = HotelSerializer(hotel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if hotel:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        '''Delete a hotel. Only staff can delete a hotel'''
        user = request.user
        if not user.is_staff:
            return Response({'message': 'You are not authorized to delete a hotel'}, status=status.HTTP_401_UNAUTHORIZED)
        hotel_id = request.data.get('id')
        hotel = Hotel.objects.filter(id=hotel_id).first()
        if hotel:
            hotel.delete()
            return Response({'message': 'Hotel deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Hotel not found'}, status=status.HTTP_404_NOT_FOUND)