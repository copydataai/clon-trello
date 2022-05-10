

# Django
from django.db.models import BooleanField, ForeignKey, CASCADE

# Models
from trello.lists.models import List

# Utils
from trello.utils.models import TrelloModel


class SpaceWork(TrelloModel):
    """The """

    is_public = BooleanField(default=True)
    lists = ForeignKey(List, CASCADE)
