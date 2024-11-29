from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from abc_back.api.views import MultiSerializerViewSetMixin
from abc_back.containers import Container
from abc_back.products.models import Category, Product
from abc_back.products.repositories import CategoryRepository, ProductRepository

from . import openapi
from .serializers import CategoryTreeSerializer, ProductSerializer, ProductShortSerializer


class CategoryViewSet(
    MultiSerializerViewSetMixin,
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
):
    queryset = Category.objects.none()
    serializer_classes = {
        "retrieve": CategoryTreeSerializer,
        "featured": CategoryTreeSerializer,
    }
    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser]
    lookup_field = "slug"

    @inject
    def get_queryset(
        self, *, category_repository: CategoryRepository = Provide[Container.product_package.category_repository],
    ):
        return category_repository.get_featured()

    @openapi.list_categories
    @action(detail=False, methods=["GET"], url_path="featured")
    def featured(
        self, request: Request, *args,
        category_repository: CategoryRepository = Provide[Container.product_package.category_repository],
        **kwargs,
    ):
        feature_categories = category_repository.get_featured()
        serializer = self.get_serializer(feature_categories, many=True)
        return Response(serializer.data)

    @openapi.info_category
    def retrieve(self, request, *args, **kwargs):
        return super(CategoryViewSet, self).retrieve(request, *args, **kwargs)


class ProductViewSet(
    MultiSerializerViewSetMixin,
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Product.objects.none()
    serializer_classes = {
        "list": ProductShortSerializer,
        "retrieve": ProductSerializer,
    }

    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser]
    lookup_field = "slug"

    @inject
    def get_queryset(
        self, *, product_repository: ProductRepository = Provide[Container.product_package.product_repository],
    ):
        return product_repository.get_active()

    @inject
    def get_object(
        self, *, product_repository: ProductRepository = Provide[Container.product_package.product_repository],
        slug: str = None,
    ):
        print(slug)
        return product_repository.get_by_slug(slug, active=True)

    @openapi.list_products
    def list(self, request, *args, **kwargs):
        return super(ProductViewSet, self).list(request, *args, **kwargs)

    @openapi.info_product
    def retrieve(self, request, *args, **kwargs):
        product = self.get_object(**kwargs)
        serializer = self.get_serializer(product)
        return Response(serializer.data)
