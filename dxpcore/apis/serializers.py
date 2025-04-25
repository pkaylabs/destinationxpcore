from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import User

from .models import Blog, Hotel, Political, TouristSite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and ((hasattr(user, "deleted") and user.deleted == False) or not hasattr(user, "deleted")):
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    

class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    class Meta:
        model = User
        fields = ('email', 'phone', 'password', 'name', 'address',)
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure the password is not included in responses
            'email': {'required': True},       # Email is required during registration
            'phone': {'required': True},       # Phone is required during registration
        }

    def validate(self, attrs):
        """Validate the data to ensure the email and phone are unique."""
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError("Email already exists")
        if User.objects.filter(phone=attrs.get('phone')).exists():
            raise serializers.ValidationError("Phone already exists")
        return attrs

    def create(self, validated_data):
        """Create a new user instance."""
        user = User.objects.create_user(
            phone=validated_data.get('phone'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            name=validated_data.get('name'),
            address=validated_data.get('address'),
        )
        return user


class HotelSerializer(serializers.ModelSerializer):
    '''Hotel Serializer'''
    class Meta:
        model = Hotel
        exclude = ["created_at", "updated_at"]


class PoliticalSerializer(serializers.ModelSerializer):
    '''Political Serializer'''
    class Meta:
        model = Political
        exclude = ["created_at", "updated_at"]


class TouristSiteSerialiser(serializers.ModelSerializer):
    '''Tourist Attraction Site Serializers'''
    class Meta:
        model = TouristSite
        exclude = ["created_at", "updated_at"]

class BlogSerializer(serializers.ModelSerializer):
    '''Blog Serializer'''
    writer_name = serializers.CharField(source='writer.name', read_only=True)
    class Meta:
        model = Blog
        exclude = ["created_at", "updated_at"]