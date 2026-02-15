from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/',  ProfileView.as_view(), name='update-profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Add this
    path('',HomepageView.as_view(),name='home'),
    path('home/',HomeView.as_view(),name='homepage')
]