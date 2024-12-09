from django.urls import include, path
from rest_framework.routers import SimpleRouter

from abc_back.api.v1.pages.views import AboutUsViewSet, ContactViewSet, DeliveryViewSet, GiftCertificateViewSet


app_name = "pages"
manager_calendar_base_name = "pages"


router = SimpleRouter(trailing_slash=False)
router.register("about_us", AboutUsViewSet, basename="about_us")
router.register("delivery", DeliveryViewSet, basename="delivery")
router.register("gift_certificate", GiftCertificateViewSet, basename="gift_certificate")
router.register("contact", ContactViewSet, basename="contact")

urlpatterns = [
    path("", include(router.urls)),
]
