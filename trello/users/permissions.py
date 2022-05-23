

# DRF
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Allow access only to objects owned by the request user"""

    def has_object_permission(self, request, view, obj):
        return  request.user == obj
