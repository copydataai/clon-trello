

# DRF
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

# Serializers
from trello.space_works.serializers.lists import AddListSerializer, ListModelSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from trello.space_works.permissions.memberships import IsActiveSpaceWorkMember, IsAdminSpaceWorkMember

# Model
from trello.space_works.models import List, SpaceWork

class ListViewSet(viewsets.ModelViewSet):
    """List view set"""

    serializer_class = ListModelSerializer
    lookup_field: str = 'name'

    def dispatch(self, request, *args, **kwargs):
        """Verify that the space work exists"""
        slug_name = kwargs['slug_name']
        self.space_work = get_object_or_404(SpaceWork, slug_name=slug_name)
        return super(ListViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permissions based on action"""
        permissions = [IsAuthenticated]
        if self.action in ['create', 'destroy']:
            permissions.append(IsAdminSpaceWorkMember)
        elif self.action in ['update', 'retrieve']:
            permissions.append(IsActiveSpaceWorkMember)
        return [p() for p in permissions]

    def get_queryset(self):
        """Return lists from space works"""
        return List.objects.filter(space_work=self.space_work)

    def create(self, request, *args, **kwargs):
        """Handle list creation"""
        serializer = AddListSerializer(
            data=request.data,
            context={'space_work': self.space_work}
        )
        serializer.is_valid(raise_exception=True)
        list = serializer.save()
        data = self.get_serializer(list).data
        return Response(data, status=status.HTTP_201_CREATED)
