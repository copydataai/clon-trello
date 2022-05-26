

# DRF
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from trello.space_works.permissions.memberships import IsAdminSpaceWorkMember

# Serializers
from trello.space_works.serializers.space_works import SpaceWorkModelSerializer

# Filters
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

# Models
from trello.space_works.models import SpaceWork, Membership

class SpaceWorkViewSet(viewsets.ModelViewSet):
    """Space work view set"""
    serializer_class = SpaceWorkModelSerializer
    lookup_field: str = 'slug_name'

    # Filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend,)
    search_fields = ('slug_name', 'name',)
    ordering_fields = ('name', 'created', )
    filter_fields = ('created', )

    def get_queryset(self):
        """Restrict list to public-only"""
        queryset = SpaceWork.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset

    def get_permissions(self):
        if self.action == 'list':
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'create']:
            permissions = [IsAuthenticated]
        else :
            permissions = [IsAuthenticated, IsAdminSpaceWorkMember]
        return [p() for p in permissions]

    def perform_create(self, serializer):
        space_work = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            space_work=space_work,
            is_admin=True,
        )
