from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, PostViewSet


app_name = "blogs"
manager_calendar_base_name = "blogs"


router = SimpleRouter(trailing_slash=False)
router.register("category", CategoryViewSet, basename="category")
router.register("post", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]
