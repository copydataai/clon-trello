from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Utils
from trello.utils.models import TrelloModel


class User(TrelloModel, AbstractUser):
    """
    Default custom user model for clon-trello.
    """

    email = EmailField("email address", unique=True)

    USERNAME_FIELD: str = "email"

    required = ("username", "first_name" , "last_name", )



    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
