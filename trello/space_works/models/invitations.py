

# Django
from django.db import models

# Utils
from trello.utils.models import DateModel

# Managers
from trello.space_works.managers.invitations import InvitationManager

class Invitation(DateModel):
    """"""

    code = models.CharField(max_length=50, unique=True)

    issued_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        help_text='Space Work member that is providing the invitation',
        related_name='issued_by'
    )
    used_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        help_text='User that used the code to enter the space work'
    )

    space_work = models.ForeignKey(
        'space_works.SpaceWork',
        on_delete=models.CASCADE
    )

    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(blank=True, null=True)

    # Manager
    objects = InvitationManager()

    def __str__(self) -> str:
        return f"#{self.space_work.slug_name}: {self.code}"
