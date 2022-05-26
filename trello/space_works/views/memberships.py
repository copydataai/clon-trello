

# DRF
from django.core.checks import messages
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

# Models
from trello.space_works.models.space_works import SpaceWork
from trello.space_works.models.memberships import Membership
from trello.space_works.models.invitations import Invitation

# Permissions
from rest_framework.permissions import IsAuthenticated
from trello.space_works.permissions.memberships import (IsActiveSpaceWorkMember,
                                                        IsAdminSpaceWorkMember,
                                                        IsSelfMember)

# Serializers
from trello.space_works.serializers.memberships import (InvitationCreateSerializer, MembershipModelSerializer,
                                                        AddMemberSerializer)


class MembershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Space works membership view set"""

    serializer_class = MembershipModelSerializer
    lookup_field: str = 'username'

    def dispatch(self, request, *args, **kwargs):
        """Verify that the space work exists"""
        slug_name = kwargs['slug_name']
        self.space_work = get_object_or_404(SpaceWork, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permissions based on action"""
        permissions = [IsAuthenticated]
        if self.action != 'create':
            permissions.append(IsActiveSpaceWorkMember)
        if self.action == 'destroy':
            permissions.append(IsAdminSpaceWorkMember)
        elif self.action == 'invitations':
            permissions.append(IsSelfMember)
        return [p() for p in permissions]

    def get_queryset(self):
        """Return space works members"""
        return Membership.objects.filter(
            space_work=self.space_work,
            is_active=True
        )

    def get_object(self):
        """Return the space work member by using the user's username"""
        return get_object_or_404(
            Membership,
            user__username=self.kwargs['username']
        )


    def perform_destroy(self, instance):
        """Disable membership"""
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['get', 'post'])
    def invitations(self, request, *args, **kwargs):
        """Retrieve a number's invitation breakdown.

        Will return a list containing all the members that have
        used its invitations and another list containing the
        invitations that haven't being used yet.
        """

        if request.method == 'POST':
            """Create invitations"""
            serializer = InvitationCreateSerializer(
                data=request.data,
                context={'space_work': self.space_work, 'request': request}
                )
            serializer.is_valid(raise_exception=True)
            invitation = serializer.save()
            # TODO add taskapp to send email to invitation with code
            data = {
                'issued_by': invitation.issued_by.username,
                'space_work': invitation.space_work.slug_name,
            }
            return Response(data, status=status.HTTP_201_CREATED)

        invited_members = Membership.objects.filter(
            space_work=self.space_work,
            invited_by=request.user,
            is_active=True
        )
        data = {
            'used_invitations': MembershipModelSerializer(invited_members, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Handle member creation from invitation code"""
        serializer = AddMemberSerializer(
            data=request.data,
            context={'space_work': self.space_work, 'request': request}
        )
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        data = self.get_serializer(member).data
        return Response(data, status=status.HTTP_201_CREATED)
