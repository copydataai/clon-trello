

# Django
from django.utils import timezone

# DRF
from rest_framework import serializers

# Serializers
from trello.users.serializers.users import UserModelSerializer

# Models
from trello.space_works.models.memberships import Membership
from trello.space_works.models.invitations import Invitation

class MembershipModelSerializer(serializers.ModelSerializer):
    """Membership model serializer"""
    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source='created', read_only=True)
    class Meta:
        model = Membership
        fields = ('user', 'is_admin',
                  'is_active', 'invited_by',
                  'joined_at',)

        read_only_fields = (
            'user', 'invited_by',
            'joined_at',
            )


class AddMemberSerializer(serializers.Serializer):
    """
    Add member serializer.
    Handle the addition of a new member to a space work.
    Space work object must be provided in the context.
    """

    invitation_code = serializers.CharField(min_length=8)

    # user = serializers.HiddenField(required=False, default=None)
    user = serializers.HiddenField(required=False, default=serializers.CurrentUserDefault())


    def validate_user(self, data):
        """Verify user isn't already a member"""
        space_work = self.context['space_work']
        user = data
        q = Membership.objects.filter(space_work=space_work, user=user)
        if q.exists():
            raise serializers.ValidationError('User is already member of this space work')
        return data

    def validate_invitation_code(self, data):
        """Verify code exists and that it is related to the space work"""

        try:
            invitation = Invitation.objects.get(
                code=data,
                space_work=self.context['space_work'],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid invitation code.')
        self.context['invitation'] = invitation
        return data

    def create(self, data):
        """Create new space work member"""
        space_work = self.context['space_work']
        invitation = self.context['invitation']

        if 'user' not in data:
            user = self.context['request'].user
        else:
            user = data['user']

        now = timezone.now()

        # Member creation
        member = Membership.objects.create(
            user=user,
            profile=user.profile,
            space_work=space_work,
            invited_by=invitation.issued_by
        )

        # Update invitation
        invitation.used_by = user
        invitation.used = True
        invitation.used_at = now
        invitation.save()

        return member

class InvitationCreateSerializer(serializers.Serializer):

    email = serializers.EmailField()

    code = serializers.CharField(required=False)

    issued_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    space_work = serializers.HiddenField(default=None)

    def validate_user(self, data):
        """Verify user isn't already a member"""
        space_work = self.context['space_work']
        user = data
        q = Membership.objects.filter(space_work=space_work, user=user)
        if q.exists():
            raise serializers.ValidationError('User is already member of this space work')

    def create(self, data):
        """Create invitation"""
        space_work = self.context['space_work']

        if 'user' not in data:
            user = self.context['request'].user
        else:
            user = data['user']
        invitation = Invitation.objects.create(
            issued_by=user,
            space_work=space_work,
            )

        return invitation
