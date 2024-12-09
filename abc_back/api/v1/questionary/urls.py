from django.urls import include, path
from rest_framework.routers import SimpleRouter

from abc_back.api.v1.questionary.views import AboutMeViewSet, GiftCertificateOrderViewSet, QuestionViewSet


app_name = "questionary"
manager_calendar_base_name = "questionary"

router = SimpleRouter(trailing_slash=False)
router.register("about-me", AboutMeViewSet, basename="about_me")
router.register("gift-certificate-order", GiftCertificateOrderViewSet, basename="gift_certificate_order")
router.register("question", QuestionViewSet, basename="question")

urlpatterns = [
    path("", include(router.urls)),
]
