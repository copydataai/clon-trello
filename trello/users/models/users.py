"""User model"""

# Typing
from typing import List

# Django
from django.contrib.auth.models import AbstractUser
from django.db.models import fields

# Utils
from trello.utils.models import DateModel


class User(DateModel, AbstractUser):
    """User model.
    Extend from Django's Abstract User, change
    the username field to email and add some extra fields.
    adding:
        + created: DateTimeField
        + modified: DateTimeField
    """
    email = fields.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': "An user with that email already exists."
        })

    USERNAME_FIELD: str = 'email'

    REQUIRED_FIELDS: List[str] = ['first_name', 'last_name', 'username']

    is_client = fields.BooleanField('client', default=True)
    is_verified = fields.BooleanField('verified', default=False)

    def __str__(self):
        return str(self.username)
