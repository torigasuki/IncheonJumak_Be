from .models import User,Verify,Profile

from decouple import config

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserCreateSerializer,CustomTokenObtainPairSerializer,ProfileSerializer,UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from threading import Timer
import re
import requests
EMAIL_REGEX = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")

# Create your views here.
class SendEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    @classmethod
    def timer_delet(*input_string):
        try:
            target = input_string[1]
            email_list=Verify.objects.filter(email=target)
            email_list.delete()
        except:
            pass
    
    def post(self,request):
        email = request.data.get('email',None)
        if email is None:
            return Response({'error':'이메일은 필수입력항목입니다'},status=status.HTTP_400_BAD_REQUEST)
        elif not EMAIL_REGEX.match(email):
            return Response({'error':'이메일 형식이 아닙니다'},status=status.HTTP_400_BAD_REQUEST) #없으면 이메일보내는거에서 에러가 발생
        else:
            try:
                user = get_object_or_404(User,email=email)
                return Response({'error':'email already exists'},status=status.HTTP_400_BAD_REQUEST)
            except:
                subject = '인천 주막 인증코드 메일입니다.'
                from_email = config('EMAIL')
                code = get_random_string(length=6)
                if Verify.objects.filter(email=email).exists():
                    email_list=Verify.objects.filter(email=email)
                    email_list.delete()
                html_content = render_to_string('email_verfication.html', {'code': code}) 
                verify_email = EmailMessage(subject, html_content, from_email, [email]) 
                verify_email.content_subtype = 'html' 
                verify_email.send()
                Verify.objects.create(email=email,code=code)
                
                timer = 600
                # Timer(timer,self.timer_delet,(email,)).start() #테스트코드에서 있으면 10분동안 멈춤
                
                return Response({'code':code},status=status.HTTP_200_OK) #테스트용
                # return Response({'success':'success'},status=status.HTTP_200_OK)

class VerificationEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        email = request.data.get('email',None)
        code = request.data.get('code',None)
        if email is None or code is None:
            return Response({'error':'이메일이나 코드가 입력이 안되어있습니다'},status=status.HTTP_400_BAD_REQUEST)
        else:
            verify = Verify.objects.filter(email=email,code=code).first()
            if verify:
                verify.verification = True
                verify.save()
                return Response({'success':'success'},status=status.HTTP_200_OK)
            else:
                return Response({'error':'인증 코드가 틀렸습니다'},status=status.HTTP_400_BAD_REQUEST)
            
class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Profile.objects.create(user=user)
        return Response({'message':"회원가입이 완료되었습니다"}, status=status.HTTP_201_CREATED)
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        me = request.user
        profile=Profile.objects.get(user=me)
        return Response({'user': UserSerializer(me).data, 'profile': ProfileSerializer(profile).data}, status=status.HTTP_200_OK)
