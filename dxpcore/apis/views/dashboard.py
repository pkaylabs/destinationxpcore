from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PingAPI(APIView):
    '''This view is used to check if the server is up and running'''
    def get(self, request):
        '''This method is used to check if the server is up and running'''
        return Response({'message': 'pong'}, status=status.HTTP_200_OK)
