

# Django
from django.db.models import (Model, CharField, DateTimeField, TextField)



class TrelloModel(Model):
    """An abstract model
    include
    name description CharField
    created_at modified_at DateTimeField
    """
    name = CharField(max_length=100)
    description = TextField(max_length=500)
    created_at = DateTimeField()
    modified_at = DateTimeField()


    class Meta:
        abstract = True
        ordering = ('-created_at', '-modified_at',)
