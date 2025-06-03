from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.models import Blog, Hotel, TouristSite
from apis.serializers import BlogSerializer, HotelSerializer, TouristSiteSerialiser


class PingAPI(APIView):
    '''This view is used to check if the server is up and running'''
    def get(self, request):
        '''This method is used to check if the server is up and running'''
        return Response({'message': 'pong'}, status=status.HTTP_200_OK)
    

class DashboardDataAPI(APIView):
    '''This view is used to get the dashboard data'''
    def get(self, request):
        '''
        This method is used to get the dashboard data
        for the mobile app dashboard
        '''
        hotels = Hotel.objects.all().order_by('-created_at')[:5]
        # suggested blogs
        blogs = Blog.objects.all().order_by('-created_at')[:5]
        # suggested sites
        tourist_sites = TouristSite.objects.all().order_by('-created_at')[:5]
        data = {
            'hotels': HotelSerializer(hotels, many=True).data,
            # 'suggested_blogs': BlogSerializer(blogs, many=True).data,
            'tourist_sites': TouristSiteSerialiser(tourist_sites, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)
