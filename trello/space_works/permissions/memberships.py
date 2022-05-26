

# DRF
from rest_framework.permissions import BasePermission

# Models
from trello.space_works.models.memberships import Membership

class IsActiveSpaceWorkMember(BasePermission):
    """
    Allow access only to space works members.

    Expect that the views implementing this permission
    have a 'space_work' attribute assigned.
    """

    def has_permission(self, request, view):
        try:
            Membership.objects.get(
                user=request.user,
                space_work=view.space_work,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True


class IsAdminSpaceWorkMember(BasePermission):
    """
    Allow access only to admin space work member
    """

    def has_permission(self, request, view) -> bool:
        try:
            Membership.objects.get(
                user=request.user,
                space_work=view.space_work,
                is_active=True,
                is_admin=True
            )
        except Membership.DoesNotExist:
            return False
        return True

class IsSelfMember(BasePermission):
    """Allow access only to the owner of the invitations"""

    def has_permission(self, request, view) -> bool:
        """Let object permission grant access"""
        obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj) -> bool:
        """Allow acces only if member is owned by the requesting user"""
        return request.user == obj.user
