


# Django
from django.db import models

# models
from trello.users.models.users import User

# utils
from trello.utils.models import DateModel

class Profile(DateModel):
    """Profile relation to User one to one field
    marked created, modified
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Profile
    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )
    biography = models.TextField(max_length=500)


    def __str__(self):
        return str(self.user)
