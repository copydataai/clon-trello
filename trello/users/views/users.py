



# DRF
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from trello.space_works.models.space_works import SpaceWork
from trello.space_works.serializers.space_works import SpaceWorkModelSerializer
from trello.users.serializers.profile import ProfileModelSerializer

# Serializers
from trello.users.serializers.users import (UserModelSerializer,
                                            UserLoginSerializer,
                                            UserSignUpSerializer)

# Models
from trello.users.models.users import User

# Permissions
from trello.users.permissions import IsAccountOwner


class UserViewSet(RetrieveModelMixin,
                  UpdateModelMixin,
                  GenericViewSet):
    """User view set"""
    serializer_class = UserModelSerializer
    queryset = User.objects.filter(is_client=True)
    lookup_field: str = "username"


    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'profile']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': {
                'refresh_token': str(token),
                'access_token': str(token.access_token)
            }
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up"""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Update profile data"""
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response"""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        space_works = SpaceWork.objects.filter(
            members=request.user,
            membership__is_active=True
        )
        data = {
            'user': response.data,
            'space_works': SpaceWorkModelSerializer(space_works, many=True).data
        }
        response.data = data
        return response
