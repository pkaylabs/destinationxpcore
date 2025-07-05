from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.models import Notification
from apis.serializers import NotificationSerializer


class NotificationsListAPI(APIView):
    '''Notification List API endpoint'''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        '''Get all notifications. Everyone can view the notifications'''
        user = request.user
        if user.is_staff or user.is_superuser:
            # staff users can view all notifications.
            notifications = Notification.objects.all().order_by('-created_at')
        else:
            notifications = Notification.objects.none()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''Create a new notification. Only staff users can create a notification'''
        user = request.user
        if not user.is_staff or not user.is_superuser:
            return Response({'message': 'You are not authorized to create a notification'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response({"message": "Notification created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        '''Update a notification. Only staff can update a notification'''
        user = request.user
        if not user.is_staff or not user.is_superuser:
            return Response({'message': 'You are not authorized to update a notification'}, status=status.HTTP_401_UNAUTHORIZED)
        notification_id = request.data.get('id')
        notification = Notification.objects.filter(id=notification_id).first()
        if not notification:
            return Response({'message': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = NotificationSerializer(notification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Notification updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        '''Delete a notification. Only staff can delete a notification'''
        user = request.user
        if not user.is_staff or not user.is_superuser:
            return Response({'message': 'You are not authorized to delete a notification'}, status=status.HTTP_401_UNAUTHORIZED)
        notification_id = request.data.get('notification')
        notification = Notification.objects.filter(id=notification_id).first()
        if notification:
            notification.delete()
            return Response({'message': 'Notification deleted successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)