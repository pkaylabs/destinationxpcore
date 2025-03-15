from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apis.models import Political
from apis.serializers import PoliticalSerializer


class PoliticalListAPI(APIView):
    '''Political List API endpoint'''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        '''Get all political. Everyone can view the political'''
        political = Political.objects.all().order_by('-created_at', 'name')
        serializer = PoliticalSerializer(political, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''Create a new Political. Only staff can create a site'''
        user = request.user
        if not user.is_staff:
            return Response({'message': 'You are not authorized to create a political site'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = PoliticalSerializer(data=request.data)
        site_id = request.data.get('id')
        political = None
        if site_id:
            political = Political.objects.filter(id=site_id).first()
            if political:
                serializer = PoliticalSerializer(political, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if political:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        '''Delete a political site. Only staff can delete a site'''
        user = request.user
        if not user.is_staff:
            return Response({'message': 'You are not authorized to delete a political site'}, status=status.HTTP_401_UNAUTHORIZED)
        site_id = request.data.get('id')
        site = Political.objects.filter(id=site_id).first()
        if site:
            site.delete()
            return Response({'message': 'Political site deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Political site not found'}, status=status.HTTP_404_NOT_FOUND)