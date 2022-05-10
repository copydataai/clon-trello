
# Django
from django.db.models import ForeignKey, CASCADE

# Models
from trello.cards.models import Card
# utils
from trello.utils.models import TrelloModel


class List(TrelloModel):
    """List Model"""

    cards = ForeignKey(Card, CASCADE)
