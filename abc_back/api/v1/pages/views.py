from __future__ import annotations

from dependency_injector.wiring import Provide
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from abc_back.api.views import MultiSerializerViewSetMixin
from abc_back.containers import Container
from abc_back.pages.models import AboutUs, Contact, Delivery, GiftCertificate
from abc_back.pages.repositories import PageRepository

from .serializers import AboutUsSerializer, ContactSerializer, DeliverySerializer, GiftCertificateSerializer


class AboutUsViewSet(MultiSerializerViewSetMixin, viewsets.GenericViewSet):
    queryset = AboutUs.objects.filter(is_featured=True)
    authentication_classes = []

    serializer_classes = {
        "featured": AboutUsSerializer,
    }

    @action(detail=False, methods=["GET"], url_path="featured")
    def featured(
        self, request: Request,
        page_repository: PageRepository = Provide[Container.page_package.page_repository],
    ):
        about_us = page_repository.get_featured_about_us()
        serializer = self.get_serializer(about_us)
        return Response(serializer.data)


class DeliveryViewSet(MultiSerializerViewSetMixin, viewsets.GenericViewSet):
    queryset = Delivery.objects.filter(is_featured=True)
    authentication_classes = []

    serializer_classes = {
        "featured": DeliverySerializer,
    }

    @action(detail=False, methods=["GET"], url_path="featured")
    def featured(
        self, request: Request,
        page_repository: PageRepository = Provide[Container.page_package.page_repository],
    ):
        delivery = page_repository.get_featured_delivery()
        serializer = self.get_serializer(delivery)
        return Response(serializer.data)


class GiftCertificateViewSet(MultiSerializerViewSetMixin, viewsets.GenericViewSet):
    queryset = GiftCertificate.objects.filter(is_featured=True)
    authentication_classes = []

    serializer_classes = {
        "featured": GiftCertificateSerializer,
    }

    @action(detail=False, methods=["GET"], url_path="featured")
    def featured(
        self, request: Request,
        page_repository: PageRepository = Provide[Container.page_package.page_repository],
    ):
        gift_certificate = page_repository.get_featured_gift_certificate()
        serializer = self.get_serializer(gift_certificate)
        return Response(serializer.data)


class ContactViewSet(MultiSerializerViewSetMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.filter(is_featured=True)
    authentication_classes = []

    serializer_classes = {
        "featured": ContactSerializer,
    }

    @action(detail=False, methods=["GET"], url_path="featured")
    def featured(
        self, request: Request,
        page_repository: PageRepository = Provide[Container.page_package.page_repository],
    ):
        contact = page_repository.get_featured_contact()
        serializer = self.get_serializer(contact)
        return Response(serializer.data)
