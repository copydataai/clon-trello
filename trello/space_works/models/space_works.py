

# Django
from django.db import models
from django.urls import reverse

# Models
from trello.users.models.users import User

# Utils
from trello.utils.models import TrelloModel


class SpaceWork(TrelloModel):
    """Space Work model.
    A space work is private in public

    """
    slug_name = models.SlugField(unique=True, max_length=40)

    members = models.ManyToManyField(
        'users.User',
        through='space_works.Membership',
        through_fields=('space_work', 'user')
        )

    is_public = models.BooleanField(default=True)

    def get_absolute_url(self):
        """Get url for space_work detail view
        return slug_name
        """
        return reverse("space-works:detail", kwargs={"slug_name": self.slug_name})

