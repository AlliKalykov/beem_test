from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import FavoriteProductViewSet


app_name = "favorites"
manager_calendar_base_name = "favorites"


router = SimpleRouter(trailing_slash=False)
router.register("product", FavoriteProductViewSet, "product")

urlpatterns = [
    path("", include(router.urls)),
]
