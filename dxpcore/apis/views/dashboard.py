import random
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from apis.models import Blog, BlogView, Hotel, Political, TouristSite
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
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
         # Convert to list of objects
        blogs_by_category_list = [
            {
                'category': category,
                'value': len(blogs),
                'color': colors[i % len(colors)]
            }
            for i, (category, blogs) in enumerate(blogs_by_category.items())
        ]

        views_by_day = [
                {
                    'day': days[i - 1],
                    'percentage': BlogView.objects.filter(created_at__week_day=i).count() / BlogView.objects.count() * 100 if BlogView.objects.count() > 0 else 0,
                    'status': 'Has Views' if BlogView.objects.filter(created_at__week_day=i).count() > 0 else 'No Views',
                    'views': BlogView.objects.filter(created_at__week_day=i).count()
                }
                for i in range(1, 8)
            ]
        
        # min and max values for views - Bar Chart
        min_max_views = {
            'min_views': min([dict(view).get('views', 0) for view in views_by_day]),
            'max_views': max([dict(view).get('views', 0) for view in views_by_day])
        }

        # yaxis labels for the bar chart [0, 20, 40, 60, 80, 100] (scaled to max views)
        yaxis_labels = [i for i in range(0, min_max_views.get('max_views', 0), min_max_views.get('max_views', 0) // 5 + 1 if min_max_views.get('max_views', 0) > 0 else 1)]

        data = {
            # top cards
            'content_upload': blogs_count + hotels_count + tourist_sites_count + political_sites_count,
            'blog_posts': Blog.objects.count(),
            'views': BlogView.objects.count(),
            'users': User.objects.count(),

            # blog views by days [mon, tue, wed, thu, fri, sat, sun]
            'views_by_day': views_by_day,

            'min_max_views': min_max_views,
            'yaxis_labels': yaxis_labels,
            
            # blogs by category
            'blogs_by_category': blogs_by_category_list,

        }
        return Response(data, status=status.HTTP_200_OK)