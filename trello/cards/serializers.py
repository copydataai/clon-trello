

# DRF
from rest_framework.serializers import ModelSerializer

# Models
from trello.cards.models import Card

class CardModelSerializer(ModelSerializer):

    class Meta:
        model = Card
        fields = ('name', 'description')
        read_only = ("name", "description", "created_at", "modified_at",)
