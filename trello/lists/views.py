

# DRF
from rest_framework.viewsets import ModelViewSet

# Models
from trello.lists.models import List

# Serializers
from trello.lists.serializers import ListSerializer



class ListViewSet(ModelViewSet)
