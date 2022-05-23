

# UUID
import uuid as uuid_lib

# Django
from django.db.models import (Model, CharField,
                              DateTimeField, TextField,
                              UUIDField)


class DateModel(Model):
    """An abstract model just for
        + created DateTimeField
        + modified DateTimeField
    """
    # DateTime fields
    created = DateTimeField('created at', auto_now_add=True)
    modified = DateTimeField('modified at', auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created', '-modified',)


class TrelloModel(DateModel):
    """An abstract model
    uuid for primary key using uuid5
    name description CharField
    """

    # PK
    uuid = UUIDField(
        primary_key=True,
        default=uuid_lib.uuid4,
        editable=False
        )

    # Char and Text Fields
    name = CharField(max_length=100)
    description = TextField(max_length=500)

    class Meta:
        abstract = True
