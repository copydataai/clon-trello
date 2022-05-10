

# DRF
from rest_framework.serializers import ModelSerializer

# Models
from trello.lists.models import List


class ListModelSerializer(ModelSerializer):
    """List Model Serializer"""

    class Meta:
        model = List
        fields = ('name', 'description',)
        read_only = ('name', 'description', 'created_at', 'modified_at')
