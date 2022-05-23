

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# models
from trello.users.models import User, Profile


class UserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_client", "is_staff",)
    search_fields = ("first_name", "last_name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin"""
    list_display = ('user',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name',)


admin.site.register(User, UserAdmin)
