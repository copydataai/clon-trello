
# Django
from django.conf import settings

# DRF
from rest_framework.routers import DefaultRouter, SimpleRouter

# ViewSets
from trello.users.views.users import UserViewSet
from trello.space_works.views.space_works import SpaceWorkViewSet
from trello.space_works.views.memberships import MembershipViewSet
from trello.space_works.views.lists import ListViewSet



if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('users', UserViewSet, basename="users")
router.register('space-works', SpaceWorkViewSet, basename="space_works")
router.register('space-works/(?P<slug_name>[-a-zA-Z0-9_]+)/members',
                MembershipViewSet,
                basename='membership')
router.register('space-works/(?P<slug_name>[-a-zA-Z0-9_]+)/lists',
                ListViewSet,
                basename='list')
# router.register('cards', CardViewSet, basename='cards')

app_name = "api"
urlpatterns = router.urls
