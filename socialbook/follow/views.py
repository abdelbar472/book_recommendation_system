# views.py
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from outh.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication  # Added for session auth


class FollowView(GenericAPIView):
    serializer_class = FollowActionSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Follow.objects.all()

    def get(self, request, username=None):
        """Get current follow status and counts"""
        try:
            user_to_check = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        is_following = Follow.objects.filter(
            follower=request.user,
            following=user_to_check
        ).exists()

        # Calculate counts
        follower_count = Follow.objects.filter(following=user_to_check).count()
        following_count = Follow.objects.filter(follower=user_to_check).count()

        return Response({
            "username": username,
            "is_following": is_following,
            "follower_count": follower_count,
            "following_count": following_count
        }, status=status.HTTP_200_OK)

    def post(self, request, username=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        follow = serializer.validated_data.get('follow', False)
        unfollow = serializer.validated_data.get('unfollow', False)

        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user_to_follow:
            return Response({"detail": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if already following
        follow_obj = Follow.objects.filter(follower=request.user, following=user_to_follow).first()

        # Calculate counts for response
        follower_count = Follow.objects.filter(following=user_to_follow).count()
        following_count = Follow.objects.filter(follower=user_to_follow).count()

        response_data = {
            "username": username,
            "follower_count": follower_count,
            "following_count": following_count
        }

        if follow and not follow_obj:
            # Not following but want to follow
            Follow.objects.create(follower=request.user, following=user_to_follow)
            response_data.update({
                "detail": f"Now following {username}",
                "is_following": True
            })
            return Response(response_data, status=status.HTTP_201_CREATED)
        elif unfollow and follow_obj:
            # Following but want to unfollow
            follow_obj.delete()
            response_data.update({
                "detail": f"Unfollowed {username}",
                "is_following": False
            })
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # No change or conflicting actions
            is_following = follow_obj is not None
            message = "Already following" if is_following else "Not currently following"
            response_data.update({
                "detail": message,
                "is_following": is_following
            })
            return Response(response_data, status=status.HTTP_200_OK)


class FollowersListView(GenericAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # Get users who follow the authenticated user
        followers = Follow.objects.filter(following=request.user).select_related('follower')
        followers_count = followers.count()
        return Response({
            'count': followers_count,
            'followers': serializer.data
        })

    def get(self, request):
        # Get users who follow the authenticated user
        followers = Follow.objects.filter(following=request.user).select_related('follower')
        followers_count = followers.count()
        serializer = self.get_serializer(followers, many=True)

        # Return both the followers data and count
        return Response({
            'count': followers_count,
            'followers': serializer.data
        })


class FollowingListView(GenericAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get_queryset(self):
        # Get users that the authenticated user follows
        return Follow.objects.filter(follower=self.request.user).select_related('following')

    def get(self, request):
        # Get users that the authenticated user follows
        following = Follow.objects.filter(follower=request.user).select_related('following')
        following_count = following.count()
        serializer = self.get_serializer(following, many=True)

        # Return both the following data and count
        return Response({
            'count': following_count,
            'following': serializer.data
        })


class UserSearchView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        if not query:
            return User.objects.none()
        return User.objects.filter(username__icontains=query)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        query = request.data.get('username', '')
        if not query:
            return Response({"results": []}, status=status.HTTP_200_OK)
        users = User.objects.filter(username__icontains=query).exclude(
            username=request.user.username
        )
        serializer = self.get_serializer(users, many=True, context={'request': request})
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)
