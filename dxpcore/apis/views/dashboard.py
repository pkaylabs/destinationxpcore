import random
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from apis.models import Blog, Hotel, Political, TouristSite
from apis.serializers import BlogSerializer, HotelSerializer, TouristSiteSerialiser


class PingAPI(APIView):
    '''This view is used to check if the server is up and running'''
    def get(self, request):
        '''This method is used to check if the server is up and running'''
        return Response({'message': 'pong'}, status=status.HTTP_200_OK)
    

class DashboardDataAPI(APIView):
    '''This view is used to get the dashboard data'''

    permission_classes = (permissions.IsAuthenticated,)

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

        # blogs count
        blogs_count = Blog.objects.count()
        # hotels count
        hotels_count = Hotel.objects.count()
        # tourist sites count
        tourist_sites_count = TouristSite.objects.count()
        # political sites count
        political_sites_count = Political.objects.count()

        # blogs by category
        blogs_by_category = {}
        blogs = Blog.objects.all()
        for blog in blogs:
            category = blog.category
            if category not in blogs_by_category:
                blogs_by_category[category] = []
            blogs_by_category[category].append(blog)

        # roybgiv colors
        colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3']

        data = {
            # top cards
            'content_upload': blogs_count + hotels_count + tourist_sites_count + political_sites_count,
            'blog_posts': Blog.objects.count(),
            'views': random.randint(1000, 5000),
            'users': User.objects.count(),
            
            # blogs by category
            'blogs_by_category': {
                # counts
                category: { 'value': len(blogs), 'color': colors[i % len(colors)] }
                for i, (category, blogs) in enumerate(blogs_by_category.items())
            },

        }
        return Response(data, status=status.HTTP_200_OK)