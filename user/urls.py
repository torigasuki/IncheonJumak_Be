from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('', views.SignUp.as_view(), name='signup'),
    path('email/', views.SendEmail.as_view(), name='send_email'),
    path('verify/', views.VerificationEmail.as_view(), name='verify_email'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]