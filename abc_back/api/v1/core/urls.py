from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CityViewSet, CountryViewSet


app_name = "core"
manager_calendar_base_name = "core"


router = SimpleRouter(trailing_slash=False)
router.register("country", CountryViewSet, basename="country")
router.register("city", CityViewSet, basename="city")


urlpatterns = [
    path("", include(router.urls)),
]
