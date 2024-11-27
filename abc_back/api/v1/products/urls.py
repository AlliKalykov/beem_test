from django.urls import include, path
from rest_framework.routers import SimpleRouter

from abc_back.api.v1.products.views import ProductViewSet


app_name = "products"
manager_calendar_base_name = "products"


router = SimpleRouter(trailing_slash=False)
router.register("", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]