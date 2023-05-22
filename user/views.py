from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
import requests
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserCreateSerializer,CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
# Create your views here.
class SignUp(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer