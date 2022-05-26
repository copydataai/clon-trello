
# Django
from django.db import models

# Models
from trello.space_works.models import SpaceWork

# utils
from trello.utils.models import TrelloModel


class List(TrelloModel):
    """List Model"""

    space_work = models.ForeignKey(SpaceWork, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
