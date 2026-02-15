# serializers.py
from rest_framework import serializers
from .models import Follow
from outh.models import User

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source='follower.username')
    following = serializers.ReadOnlyField(source='following.username')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['id', 'created_at']

class FollowActionSerializer(serializers.Serializer):

    follow = serializers.BooleanField(required=True)
    unfollow = serializers.BooleanField(required=True)


class UserSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'profile_url']

    def get_profile_url(self, obj):
        # Generate the profile URL for the user
        return f"http://127.0.0.1:8000/profile/{obj.username}/"
class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follower', 'created_at']