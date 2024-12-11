from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CartItemViewSet, CartViewSet


app_name = "cart"
manager_calendar_base_name = "cart"


router = SimpleRouter(trailing_slash=False)
router.register("item", CartItemViewSet, basename="cart_item")
router.register("", CartViewSet, basename="cart")


urlpatterns = [
    path("", include(router.urls)),
]
