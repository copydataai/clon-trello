

# DRF
from rest_framework import serializers

# Models
from trello.users.models.notifications import Notification

class NotificationModelSerializer(serializers.ModelSerializer):
    """Notification Model serializer"""


    class Meta:
        model = Notification
        fields = ('name', 'description',)
        read_only = ('created', 'modified',)
