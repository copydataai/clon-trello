

# Django
from django.contrib.auth import authenticate, password_validation

# DRF
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# SimpleJWT
from rest_framework_simplejwt.tokens import RefreshToken

# Serializers
from trello.users.serializers.profile import ProfileModelSerializer

# models
from trello.users.models import User, Profile


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer"""
    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        queryset = User.objects.filter(is_verified=True)
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'profile',)
        # extra_kwargs = {'password': {'write_only': True}}



class UserLoginSerializer(serializers.Serializer):
    """User login serializer"""

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials"""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        # if not user.is_verified:
        #     raise serializers.ValidationError("Account is not active yet.")
        self.context['user'] = user
        return data

    def create(self, data):
        token = RefreshToken.for_user(self.context['user'])
        return self.context['user'], token


class UserSignUpSerializer(serializers.Serializer):
    """User SignUp serializer"""

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(User.objects.all())]
        )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Verify and password match"""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Password don't match")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)
        return user
