import random
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from apis.models import Blog, Hotel, TouristSite
from apis.serializers import BlogSerializer, HotelSerializer, TouristSiteSerialiser


class PingAPI(APIView):
    '''This view is used to check if the server is up and running'''
    def get(self, request):
        '''This method is used to check if the server is up and running'''
        return Response({'message': 'pong'}, status=status.HTTP_200_OK)
    

class DashboardDataAPI(APIView):
    '''This view is used to get the dashboard data'''

    permission_classes = (permissions.IsAdminUser,)

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


class WebDashboardDataAPI(APIView):
    '''This view is used to get the dashboard data for the web dashboard'''

    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        '''
        This method is used to get the dashboard data
        for the web dashboard
        '''

        # blogs by category
        blogs_by_category = {}
        blogs = Blog.objects.all()
        for blog in blogs:
            category = blog.category
            if category not in blogs_by_category:
                blogs_by_category[category] = []
            blogs_by_category[category].append(blog)

        data = {
            # top cards
            'content_upload': random.randint(100, 500),
            'blog_posts': Blog.objects.count(),
            'views': random.randint(1000, 5000),
            'users': User.objects.count(),
            # blogs by category
            'blogs_by_category': {
                # counts
                category: len(blogs) for category, blogs in blogs_by_category.items()
            },

        }
        return Response(data, status=status.HTTP_200_OK)