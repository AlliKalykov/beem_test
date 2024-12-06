from __future__ import annotations

from rest_framework import mixins, viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from abc_back.api.pagination import DefaultPageNumberPagination
from abc_back.api.views import MultiSerializerViewSetMixin

from abc_back.favorites.models import FavoriteProduct

from .serializers import FavoriteProductShortSerializer, FavoriteProductSerializer


class FavoriteProductViewSet(
    MultiSerializerViewSetMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = FavoriteProduct.objects.none()
    serializer_classes = {
        "create": FavoriteProductShortSerializer,
        "list": FavoriteProductSerializer,
    }
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    pagination_class = DefaultPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return FavoriteProduct.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        favorite_product = serializer.save()
        serializer = FavoriteProductSerializer(favorite_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
