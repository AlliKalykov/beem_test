from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CartItemViewSet


app_name = "cart"
manager_calendar_base_name = "cart"


router = SimpleRouter(trailing_slash=False)
router.register("item", CartItemViewSet, basename="cart_item")


urlpatterns = [
    path("", include(router.urls)),
]
