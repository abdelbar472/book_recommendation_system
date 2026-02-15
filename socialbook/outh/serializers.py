from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_following']

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from follow.models import Follow
            return Follow.objects.filter(follower=request.user, following=obj).exists()
        return False

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    username = serializers.CharField(required=True)  # Add username field

    class Meta:
        model = User
        fields = ['email', 'username', 'password']  # Include username

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],  # Pass username
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Use email for login
    password = serializers.CharField(write_only=True)

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)  # Authenticate using email

        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        data['user'] = user
        data['tokens'] = self.get_tokens(user)
        return data

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            self.fail('bad_token')

class profileSerializer(serializers.ModelSerializer):
    profile_image = serializers.FileField(required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name','profile_image', 'bio', 'website', 'location']
        read_only_fields = ['user_id', 'email', 'followers_count', 'following_count']

# allow user to follow and unfollow other users
