from .models import User,Verify,Profile,Follow,BookMark

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

from .serializers import UserCreateSerializer,CustomTokenObtainPairSerializer,ProfileSerializer,UserSerializer,UserDetailSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from .models import User,Verify, Follow, BookMark
from django.template.loader import render_to_string
from decouple import config
from threading import Timer
import re
import requests
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

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
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email':openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
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
                Timer(timer,self.timer_delet,(email,)).start() #테스트코드에서 있으면 10분동안 멈춤
                
                return Response({'code':code},status=status.HTTP_200_OK) #테스트용
                # return Response({'success':'success'},status=status.HTTP_200_OK)

class VerificationEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'code'],
            properties={
                'email':openapi.Schema(type=openapi.TYPE_STRING),
                'code':openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
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

    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Profile.objects.create(user=user)
        return Response({'message':"회원가입이 완료되었습니다"}, status=status.HTTP_201_CREATED)
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    
KAKAO_HOST= 'https://kauth.kakao.com/'
class SocialUrlView(APIView):
    def post(self,request):
        social = request.data.get('social',None)
        if social is None:
            return Response({'error':'소셜로그인이 아닙니다'},status=status.HTTP_400_BAD_REQUEST)
        elif social == 'kakao':
            url = KAKAO_HOST + 'oauth/authorize?client_id=' + config('KAKAO_REST_API') + '&redirect_uri=' + config('REDIRECT_URI') + '&response_type=code&prompt=login'
            return Response({'url':url},status=status.HTTP_200_OK)
        elif social == 'naver':
            url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=' + config('NAVER_CLIENT_ID') + '&redirect_uri=' + config('REDIRECT_URI') + '&state=STATE_STRING'
            return Response({'url':url},status=status.HTTP_200_OK)   
        elif social == 'google':
            return Response({'key':config('GOOGLE_API_KEY'),'redirecturi':config('REDIRECT_URI')},status=status.HTTP_200_OK)
        

class KakaoLoginView(APIView):
    def post(self,request):
        code = request.data.get('code')
        print(code)
        access_token = requests.post(KAKAO_HOST+"oauth/token",
            headers={"Content-Type":"application/x-www-form-urlencoded"},
            data={
                "grant_type":"authorization_code",
                "client_id":config('KAKAO_REST_API'),
                "redirect_uri":"http://127.0.0.1:5500/index.html",
                "code":code,
            },
        )
        access_token = access_token.json().get("access_token")
        user_data_request = requests.get("https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        )
        user_datajson = user_data_request.json()
        user_data = user_datajson.get("kakao_account").get("profile")
        print(user_data)
        email = user_datajson.get('kakao_account').get('email')
        nickname = user_data.get("nickname")
        profileimage = user_data.get("profile_image_url")
        try:
            user = User.objects.get(email=email)
            if user.logintype == 'local':
                return Response({'error':'소셜로그인 가입이메일이아닙니다'},status=status.HTTP_400_BAD_REQUEST)
            else:
                refresh = RefreshToken.for_user(user)
                refresh["email"] = user.email
                refresh["nickname"] = user.nickname
                refresh['logintype'] = user.logintype
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK
                )
        except:
            user = User.objects.create_user(email=email,nickname=nickname, logintype='kakao')
            user.set_unusable_password()
            user.save()
            profile=Profile.objects.get(user=user)
            profile.profileimage = profileimage
            profile.save()
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["nickname"] = user.nickname
            refresh['logintype'] = user.logintype
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )

class NaverLoginView(APIView):
    def post(self,request):
        grant_type = 'authorization_code' # 발급
        client_id = config('NAVER_CLIENT_ID')
        client_secret = config('NAVER_CLIENT_SECRET')
        code = request.data.get('code')
        state = request.data.get('state')
        parameters = f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"
        token_request = requests.get(f"https://nid.naver.com/oauth2.0/token?{parameters}")
        token_request = token_request.json()
        access_token = token_request.get("access_token")
        user_data_request = requests.get("https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_datajson = user_data_request.json()
        user_data = user_datajson.get('response')
        email = user_data.get('email')
        nickname = user_data.get('nickname')
        profileimage = user_data.get('profile_image')
        try:
            user = User.objects.get(email=email)
            if user.logintype == 'local':
                return Response({'error':'소셜로그인 가입이메일이아닙니다'},status=status.HTTP_400_BAD_REQUEST)
            else:
                refresh = RefreshToken.for_user(user)
                refresh["email"] = user.email
                refresh["nickname"] = user.nickname
                refresh['logintype'] = user.logintype
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK
                )
        except:
            user = User.objects.create_user(email=email,nickname=nickname,logintype='naver')
            user.set_unusable_password()
            user.save()
            profile=Profile.objects.get(user=user)
            profile.profileimage = profileimage
            profile.save()
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["nickname"] = user.nickname
            refresh['logintype'] = user.logintype
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )

class GoogleLoginView(APIView):
    def post(self,request):
        access_token = request.data['code']
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_request = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
        user_data = user_info_request.json()
        print(user_data)
        
        email = user_data.get('email')
        nickname = user_data.get('name')
        profileimage = user_data.get('picture')
        try:
            user = User.objects.get(email=email)
            if user.logintype == 'local':
                return Response({'error':'소셜로그인 가입이메일이아닙니다'},status=status.HTTP_400_BAD_REQUEST)
            else:
                refresh = RefreshToken.for_user(user)
                refresh["email"] = user.email
                refresh["nickname"] = user.nickname
                refresh['logintype'] = user.logintype
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK
                )
        except:
            user = User.objects.create_user(email=email,nickname=nickname,logintype='google')
            user.set_unusable_password()
            user.save()
            profile=Profile.objects.get(user=user)
            profile.profileimage = profileimage
            profile.save()
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["nickname"] = user.nickname
            refresh['logintype'] = user.logintype
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        me = request.user
        profile=Profile.objects.get(user=me)

        user_serializer = UserSerializer(me).data
        # db요청을 최소화하기 위해 한번에 id를 가져오도록 하고, 이후에 각각 나누기
        follow_id_list = user_serializer['follower'] +user_serializer['following']
        follow_list = Follow.objects.filter(id__in=follow_id_list) 
        follower_user_id_list = [follow.follower_id for follow in follow_list if follow.follower_id != me.id]
        following_user_id_list = [follow.following_id for follow in follow_list if follow.following_id != me.id]
        followed_user = User.objects.filter(id__in=follower_user_id_list + following_user_id_list).values('id','nickname',)
        follow_user_map = {follow['id']: follow for follow in followed_user} 
        for i in range(len(follower_user_id_list)): #[2,4,6] / i = 0 1 2
            follower_user_id_list[i] = follow_user_map[follower_user_id_list[i]]
        for i in range(len(following_user_id_list)):
            following_user_id_list[i] = follow_user_map[following_user_id_list[i]]
        user_serializer['follower'] = follower_user_id_list
        user_serializer['following'] = following_user_id_list
        return Response({'user': user_serializer, 'profile': ProfileSerializer(profile).data}, status=status.HTTP_200_OK)
    
    def put(self,request):
        me = request.user
        profile=Profile.objects.get(user=me)
        serializer = ProfileSerializer(profile,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class FollowView(APIView):
    """follow를 생성/해제하는 View"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        request_user = request.user
        following_user = Follow.objects.filter(follower_id=request_user.id, following_id=user_id).last()
        if following_user:
            following_user.delete()
            return Response({"message":"팔로우 취소"}, status=status.HTTP_200_OK)
        else:
            Follow.objects.create(follower_id=request_user.id, following_id=user_id)
            return Response({"message":"팔로우"}, status=status.HTTP_200_OK)

#follow id값으로 쿼리를 반복요청하게 되기때문에 좋은 코드가 아닙니다. 참고하시되 다른 방향으로 적용하세요!
class FollowingUserView(APIView):
    """follow id로 user id 및 nickname 가져오기"""
    def get(self, request, follow_id):
        following_id_list = Follow.objects.filter(id=follow_id).values_list('following_id', flat=True)
        user = User.objects.filter(id__in=following_id_list).values('id','nickname',)
        if not user:
            return Response({'message': '아직 팔로우 정보가 없습니다.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(user, status=status.HTTP_200_OK)


class BookMarkView(APIView):
    """BookMark 생성, 취소 기능"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, alchol_id):
        bookmark = BookMark.objects.filter(marked_user_id=request.user.id, alchol_id=alchol_id).last()
        if bookmark:
            bookmark.delete()
            return Response({"message":"북마크📌 취소"}, status=status.HTTP_200_OK)
        else:
            BookMark.objects.create(marked_user_id=request.user.id, alchol_id=alchol_id)
            return Response({"message":"북마크📌"}, status=status.HTTP_200_OK)

class BookMarkListView(APIView):
    """특정 유저의 bookmark list 가져오기"""
    def get(self, request, user_id):
        bookmark = BookMark.objects.filter(marked_user_id=user_id)
        if not bookmark:
            return Response({"message":"북마크📌가 없습니다"}, status=status.HTTP_204_OK)
        else:
            return Response({'data':bookmark}, status=status.HTTP_200_OK)
        
class UserDetailView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id = user_id)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)