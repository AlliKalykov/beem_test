from django.urls import include, path
from rest_framework.routers import SimpleRouter

from abc_back.api.v1.users.views import ProfileViewSet, UserViewSet


app_name = "users"
manager_calendar_base_name = "users"


router = SimpleRouter(trailing_slash=False)
router.register("", UserViewSet, basename="user")
router.register("profile", ProfileViewSet, basename="profile")
urlpatterns = [
    path("", include(router.urls)),
]
