

# DRF
from rest_framework import serializers

# Models
from trello.space_works.models.lists import List


# Serializers


class ListModelSerializer(serializers.ModelSerializer):
    """List Model Serializer"""


    class Meta:
        model = List
        fields = ('name', 'description',)
        read_only = ('name', 'description', 'created_at', 'modified_at')

class AddListSerializer(serializers.Serializer):
    """
    Add list to space work serializer.
    Handle the addition of a new list to a space work.
    Space work object must be provided in the context.
    """

    name = serializers.CharField(min_length=10)
    description = serializers.CharField(max_length=500)

    def create(self, data):
        """Create new list in space work."""
        space_work = self.context['space_work']

        list = List.objects.create(
            name=data['name'],
            description=data['description'],
            space_work=space_work
            )
        return list
