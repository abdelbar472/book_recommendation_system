from tokenize import TokenError

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from rest_framework.authentication import SessionAuthentication
from follow.models import Follow
from follow.serializers import *


class SignupAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Optional: generate tokens here if frontend needs them on signup
            send_mail(
                subject="Welcome to the App!",
                message=f"Hi {user.username},\nWelcome to the app! Your profile setup is pending.",
                from_email='your_email@example.com',  # Replace with env var in production
                recipient_list=[user.email],
                fail_silently=True,
            )
            redirect_url = "http://127.0.0.1:8000/profile/"
            return Response({"redirect_url": redirect_url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            remember_me = serializer.validated_data.get('remember_me', False)
            login(request, user)

            if not remember_me:
                request.session.set_expiry(0)  # Browser close → logout

            tokens = serializer.validated_data['tokens']
            redirect_url = "http://127.0.0.1:8000/following/"

            return Response({
                "message": "Login successful!",
                "access_token": tokens['access'],
                "refresh_token": tokens['refresh'],
                "redirect_url": redirect_url
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LogoutAPIView(APIView):

    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]     # Public endpoint

    def post(self, request):
        # Delete Django session (kills sessionid + csrftoken)
        if request.user.is_authenticated:
            logout(request)  # ← THIS LINE KILLS THE SESSION
            request.session.flush()

        # Then delete/blacklist JWT refresh token
        refresh_token = request.COOKIES.get('refresh_token') or request.data.get('refresh_token')

        response = Response({"message": "Logged out successfully"}, status=200)

        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except:
                pass

        # Clear all cookies
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')

        return response
class ProfileView(generics.GenericAPIView):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = profileSerializer

    def get(self, request):
        user = request.user

        # Fixed: Calculate counts inside the method (was out of scope before)
        profile_data = {
            'followers_count': Follow.objects.filter(following=user).count(),
            'following_count': Follow.objects.filter(follower=user).count(),
        }

        serializer = profileSerializer(user, context={'request': request})
        response_data = serializer.data
        response_data.update(profile_data)

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Return fresh data with counts
            fresh_serializer = profileSerializer(user, context={'request': request})
            fresh_data = fresh_serializer.data
            fresh_data.update({
                'followers_count': Follow.objects.filter(following=user).count(),
                'following_count': Follow.objects.filter(follower=user).count(),
            })
            return Response(fresh_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class HomeView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({
                "data": {
                    "login_url": "http://127.0.0.1:8000/login/",
                    "signup_url": "http://127.0.0.1:8000/signup/"
                },
                "message": "Authentication required"
            }, status=status.HTTP_200_OK)

        user = request.user
        serializer = UserSerializer(user, context={'request': request})

        # Add follower counts
        data = serializer.data
        data.update({
            'followers_count': Follow.objects.filter(following=user).count(),
            'following_count': Follow.objects.filter(follower=user).count(),
        })

        return Response({
            "data": data,
            "message": "Welcome to the Home Page!"
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """Search users by username"""
        if not request.user.is_authenticated:
            return Response({
                "results": [],
                "login_url": "http://127.0.0.1:8000/login/",
                "signup_url": "http://127.0.0.1:8000/signup/"
            }, status=status.HTTP_200_OK)

        query = request.data.get('query', '').strip()
        if not query:
            return Response({"results": []}, status=status.HTTP_200_OK)

        users = User.objects.filter(username__icontains=query) \
                            .exclude(username=request.user.username)
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)



class UserProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)

            # Safely get profile fields (in case Profile model doesn't exist yet)
            bio = getattr(user, 'bio', '') if hasattr(user, 'bio') else ''
            profile_image = ''
            website = getattr(user, 'website', '') if hasattr(user, 'website') else ''
            location = getattr(user, 'location', '') if hasattr(user, 'location') else ''

            if hasattr(user, 'profile') and user.profile and user.profile.profile_image:
                profile_image = request.build_absolute_uri(user.profile.profile_image.url)

            serializer = UserSerializer(user, context={'request': request})
            data = serializer.data

            # Add counts and extra fields
            data.update({
                'followers_count': Follow.objects.filter(following=user).count(),
                'following_count': Follow.objects.filter(follower=user).count(),
                'bio': bio,
                'profile_image': profile_image,
                'website': website,
                'location': location,
            })

            return Response(data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Optional: You can keep this as a helper or remove if not used elsewhere
class HomepageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get(self, request):
        # Redirects to HomeView logic – better to just use HomeView directly
        return HomeView.as_view()(request._request)