from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.models import Blog
from apis.serializers import BlogSerializer, BlogViewSerializer


class BlogsListAPI(APIView):
    '''Blog List API endpoint'''
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        '''Get all/random blogs. Everyone can view the blogs'''
        user = request.user
        # check if user is authenticated and is staff or superuser
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            # staff users can view all blogs.
            blogs = Blog.objects.all().order_by('-created_at')
        else:
            # fetch 20 random blogs for non-staff users.
            blogs = Blog.objects.filter(is_published=True).order_by('?')[:20]
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''Create a new blog. Only staff users can create a blog'''
        user = request.user
        if not user.is_authenticated or not (user.is_staff or user.is_superuser):
            return Response({'message': 'You are not authorized to create a hotel'}, status=status.HTTP_401_UNAUTHORIZED)
        # injecting the writer id into the request data
        # so that we can save the blog with the writer id.
        # req_data = request.data.copy()
        # req_data['writer'] = user.id
        serializer = BlogSerializer(data=request.data)
        blog_id = request.data.get('id')
        blog = None
        # if blog_id is present, update it. else create a new blog.
        if blog_id:
            blog = Blog.objects.filter(id=blog_id).first()
            if blog:
                serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            if not blog:
                serializer.save(writer=user)
            else:
                serializer.save()
            if blog:
                return Response({"message": "Blog updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"message": "Blog Created Successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        '''Delete a blog. Only staff can delete a blog'''
        user = request.user
        if not user.is_authenticated or not user.is_staff:
            return Response({'message': 'You are not authorized to delete a hotel'}, status=status.HTTP_401_UNAUTHORIZED)
        blog_id = request.data.get('blog')
        blog = Blog.objects.filter(id=blog_id).first()
        if blog:
            blog.delete()
            return Response({'message': 'Blog deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
    

class ViewBlogAPI(APIView):
    '''View Blog API endpoint'''
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        '''View a blog by id. Everyone can view the blogs'''
        serializer = BlogViewSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                serializer.save(user=request.user, ip_address=request.META.get('REMOTE_ADDR'))
            else:
                serializer.save(ip_address=request.META.get('REMOTE_ADDR'))
            return Response({'message': 'Blog viewed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
