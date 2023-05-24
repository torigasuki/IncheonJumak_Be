from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('', views.SignUpView.as_view(), name='signup'),
    path('email/', views.SendEmailView.as_view(), name='send_email'),
    path('verify/', views.VerificationEmailView.as_view(), name='verify_email'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('social/', views.SocialUrlView.as_view(), name='social_login'),
    path('kakao/', views.KakaoLoginView.as_view(), name='kakao_login'),
    path('naver/', views.NaverLoginView.as_view(), name='naver_login'),
    path('google/', views.GoogleLoginView.as_view(), name='google_login'),
    #follow 기능 url
    path("<int:user_id>/follow/", views.FollowView.as_view(), name="follow_user"),
    path("<int:user_id>/followings/", views.FollowingView.as_view(), name="followings"),
    path("<int:user_id>/followers/", views.FollowerView.as_view(), name="followers"),
    #bookmark 기능 url
    path("<int:alchol_id>/bookmark/", views.BookMarkView.as_view(), name="bookmark_view"),
    path("<int:user_id>/bookmark_list/",views.BookMarkListView.as_view(),name="bookmark_list_view",),
    #profile url
    path('profile/', views.ProfileView.as_view(), name='profile'),
]