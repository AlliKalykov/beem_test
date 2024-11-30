from django.urls import include, path
from rest_framework.routers import SimpleRouter

from abc_back.api.v1.pages.views import AboutUsViewSet


app_name = "pages"
manager_calendar_base_name = "pages"


router = SimpleRouter(trailing_slash=False)
router.register("about_us", AboutUsViewSet, basename="about_us")

urlpatterns = [
    path("", include(router.urls)),
]
