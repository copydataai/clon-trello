"""Notification model"""

# Django
from django.db import models


from trello.users.models.profile import Profile

# Utils
from trello.utils.models import TrelloModel


class Notification(TrelloModel):
    """Notifications models register by signals from follows"""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
