from __future__ import annotations

from rest_framework import mixins, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from abc_back.api.pagination import DefaultPageNumberPagination
from abc_back.api.views import MultiSerializerViewSetMixin
from abc_back.favorites.models import FavoriteProduct

from .serializers import FavoriteProductSerializer


class FavoriteProductViewSet(
    MultiSerializerViewSetMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = FavoriteProduct.objects.none()
    serializer_classes = {
        "list": FavoriteProductSerializer,
    }
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    pagination_class = DefaultPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return FavoriteProduct.objects.filter(user=user)
