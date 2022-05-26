

# Django
from django.contrib import admin

# models
from trello.space_works.models import SpaceWork


@admin.register(SpaceWork)
class SpaceWorkAdmin(admin.ModelAdmin):
    list_display = ('slug_name', 'is_public', )
