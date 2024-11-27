from __future__ import annotations

from rest_framework import viewsets

from abc_back.api.views import MultiSerializerViewSetMixin, MultiThrottllesViewSetMixin
from abc_back.products.models import Product

from . import openapi
from .serializers import ProductSerializer


class ProductViewSet(
    MultiSerializerViewSetMixin,
    MultiThrottllesViewSetMixin,
    viewsets.GenericViewSet,
):
    queryset = Product.objects.none()
    serializer_classes = {
        "list": ProductSerializer,
        "retrieve": ProductSerializer,
    }

    @openapi.list_products
    def list(self, request, *args, **kwargs):
        return super(ProductViewSet, self).list(request, *args, **kwargs)

    @openapi.info_product
    def retrieve(self, request, *args, **kwargs):
        return super(ProductViewSet, self).retrieve(request, *args, **kwargs)
