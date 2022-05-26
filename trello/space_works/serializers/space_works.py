

# DRF
from rest_framework import serializers

# Model
from trello.space_works.models import SpaceWork

# Serializer
from trello.space_works.serializers.lists import ListModelSerializer

class SpaceWorkModelSerializer(serializers.ModelSerializer):
    """Space works model serializer"""
    class Meta:
        model = SpaceWork
        fields = ('name', 'slug_name',
                  'description', 'is_public',
                  )

        read_only = ('name', 'slug_name', 'description',
                     'is_public', 'created', 'modified',)
