from rest_framework.views import APIView
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import status, permissions
from django.contrib.auth import login

from accounts.models import User, OTP
from apis.serializers import UserSerializer, LoginSerializer, RegisterUserSerializer



class LoginAPI(APIView):
    '''Login api endpoint'''
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            for field in list(e.detail):
                error_message = e.detail.get(field)[0]
                field = f"{field}: " if field != "non_field_errors" else ""
                response_data = {
                    "status": "error",
                    "error_message": f"{field} {error_message}",
                    "user": None,
                    "token": None,
                }
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            user = serializer.validated_data
       
        login(request, user)

        # Delete existing token
        AuthToken.objects.filter(user=user).delete()
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1],
        })


class RegisterUserAPI(APIView):
    '''Register User api endpoint'''
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            for field in list(e.detail):
                error_message = e.detail.get(field)[0]
                field = f"{field}: " if field != "non_field_errors" else ""
                response_data = {
                    "status": "error",
                    "error_message": f"{field} {error_message}",
                    "user": None,
                    "token": None,
                }
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            user = serializer.save()
            user.is_active = True
            user.save()
            return Response({
                "user": UserSerializer(user).data,
                "token": AuthToken.objects.create(user)[1],
            })
        

class LogoutAPIView(APIView):
    '''Logout API endpoint'''
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({
            "status": "success",
            "message": "User logged out successfully",
        }, status=status.HTTP_200_OK)
    

class UsersListAPIView(APIView):
    '''List all users'''
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)
    
class UserProfileAPIView(APIView):
    '''Get user profile'''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        '''Get user profile'''
        user = request.user
        return Response(UserSerializer(user).data)
    
    def put(self, request, *args, **kwargs):
        '''Update user profile'''
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        '''Use this to disable/enable a user account. To be used by admins only'''
        user = request.user
        if user.is_superuser:
            culprit_id = request.data.get('id')
            account_status = request.data.get('is_active')
            if user.id == culprit_id:
                return Response({'message': 'You cannot disable your own account'}, status=status.HTTP_400_BAD_REQUEST)
            if not culprit_id:
                return Response({'message': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            if not (account_status == True or account_status == False):
                print(f"Account status: {account_status}")
                return Response({'message': 'Account status is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            culprit = User.objects.filter(id=culprit_id).first()
            if not culprit:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            culprit.is_active = account_status == True
            culprit.save()
            return Response(UserSerializer(culprit).data)
        return Response({'message': 'You are not authorized to disable this account'}, status=status.HTTP_401_UNAUTHORIZED)
    