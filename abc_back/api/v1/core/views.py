from __future__ import annotations

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from abc_back.api.pagination import DefaultPageNumberPagination
from abc_back.api.views import MultiSerializerViewSetMixin
from abc_back.core.models import City, Country

from .serializers import CitySerializer, CountrySerializer


class CountryViewSet(
    MultiSerializerViewSetMixin, viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
):
    queryset = Country.objects.all()
    serializer_classes = {
        "list": CountrySerializer,
        "retrieve": CountrySerializer,
    }
    authentication_classes = []
    pagination_class = DefaultPageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "position"]

    lookup_field = "slug"


class CityViewSet(
    MultiSerializerViewSetMixin, viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
):
    queryset = City.objects.all()
    serializer_classes = {
        "list": CitySerializer,
        "retrieve": CitySerializer,
    }
    authentication_classes = []
    pagination_class = DefaultPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["country"]
    search_fields = ["name", "country__name"]
    ordering_fields = ["name", "position"]

    lookup_field = "slug"
