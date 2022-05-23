

# DRF
from rest_framework import serializers

# Models
from trello.users.models.profile import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile Model serializer"""

    class Meta:
        model = Profile
        fields = ('biography', 'picture',)
