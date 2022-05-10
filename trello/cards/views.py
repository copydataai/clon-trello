

# DRF
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

# Serializer
from trello.cards.serializers import CardSerializer

# Model
from trello.cards.models import Card


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer
    queryset = Car.objects.filter(list)
    permission_classes = [permissions.IsAuthenticated]
