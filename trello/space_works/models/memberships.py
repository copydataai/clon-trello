"""Membership model"""

# Django
from django.db import models

# Utils
from trello.utils.models import DateModel
import uuid as uuid_lib


class Membership(DateModel):
    """
    Membership model.
    A membership is the table that holds the relationship between
    a user and a space_work.
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid_lib.uuid4,
        editable=False
        )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    space_work = models.ForeignKey('space_works.SpaceWork', on_delete=models.CASCADE)

    is_admin = models.BooleanField(
        'space_works admin',
        default=False,
        help_text="Space Works admins can update the space works data and manage its members"
    )

    invited_by = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='invited_by'
    )

    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text="Only active users are allowed to interact in the circle"
    )

    def __str__(self) -> str:
        """Return username and space_work"""
        return f'@{self.user.username} at #{self.space_work.slug_name}'
