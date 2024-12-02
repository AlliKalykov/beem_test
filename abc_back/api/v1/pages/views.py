from __future__ import annotations

from rest_framework import mixins, viewsets

from abc_back.api.views import MultiSerializerViewSetMixin

from .serializers import AboutUsSerializer, DeliverySerializer, GiftCertificateSerializer


class AboutUsViewSet(MultiSerializerViewSetMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = AboutUsSerializer.Meta.model.objects.all()
    permission_classes = []

    serializer_classes = {
        "retrieve": AboutUsSerializer,
    }


class DeliveryViewSet(MultiSerializerViewSetMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = DeliverySerializer.Meta.model.objects.all()
    permission_classes = []

    serializer_classes = {
        "retrieve": DeliverySerializer,
    }


class GiftCertificateViewSet(MultiSerializerViewSetMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = GiftCertificateSerializer.Meta.model.objects.all()
    permission_classes = []

    serializer_classes = {
        "retrieve": GiftCertificateSerializer,
    }
