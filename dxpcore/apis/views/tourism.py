from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.models import TouristSite
from apis.serializers import TouristSiteSerialiser


class TouristSiteListAPI(APIView):
    '''TouristSite List API endpoint'''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        '''Get all sites. Everyone can view the sites'''
        sites = TouristSite.objects.all().order_by('-created_at', 'name')
        serializer = TouristSiteSerialiser(sites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''Create a new tourist site. Only staff can create a site'''
        user = request.user
        if not user.is_staff:
            return Response({'message': 'You are not authorized to create a tourist site'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TouristSiteSerialiser(data=request.data)
        site_id = request.data.get('id')
        site = None
        if site_id:
            site = TouristSite.objects.filter(id=site_id).first()
            if site:
                serializer = TouristSiteSerialiser(site, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if site:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        '''Delete a tourist site. Only staff can delete a site'''
        user = request.user
        if not user.is_staff:
            return Response({'message': 'You are not authorized to delete a tourist site'}, status=status.HTTP_401_UNAUTHORIZED)
        site_id = request.data.get('id')
        site = TouristSite.objects.filter(id=site_id).first()
        if site:
            site.delete()
            return Response({'message': 'Tourist site deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Tourist site not found'}, status=status.HTTP_404_NOT_FOUND)