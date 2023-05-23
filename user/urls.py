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
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]