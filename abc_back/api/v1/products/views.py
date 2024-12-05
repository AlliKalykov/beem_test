from __future__ import annotations

from dependency_injector.wiring import Provide, inject
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from abc_back.api.permissions import IsSuperUser
from abc_back.api.views import MultiSerializerViewSetMixin, MultiPermissionViewSetMixin
from abc_back.containers import Container
from abc_back.products.models import Category, Product
from abc_back.products.repositories import CategoryRepository, ProductRepository

from . import openapi
from .serializers import (
    CategoryTreeSerializer, ProductSerializer, ProductShortSerializer, CategoryShortSerializer, ProductListSerializer,
    ProductUpdateSerializer,
)


class CategoryViewSet(
    MultiSerializerViewSetMixin,
    MultiPermissionViewSetMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_classes = {
        "create": CategoryShortSerializer,
        "update": CategoryShortSerializer,
        "partial_update": CategoryShortSerializer,
        "retrieve": CategoryTreeSerializer,
        "featured": CategoryTreeSerializer,
    }
    permission_action_map = {
        "create": [IsSuperUser],
        "update": [IsSuperUser],
        "partial_update": [IsSuperUser],
        "destroy": [IsSuperUser],
        "retrieve": [AllowAny],
        "featured": [AllowAny],
    }
    parser_classes = [JSONParser, MultiPartParser]
    http_method_names = ["get", "post", "patch", "delete"]
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


class ProductViewSet(
    MultiSerializerViewSetMixin,
    MultiPermissionViewSetMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Product.objects.none()
    serializer_classes = {
        "create": ProductSerializer,
        "list": ProductShortSerializer,
        "retrieve": ProductListSerializer,
        "update": ProductUpdateSerializer,
        "partial_update": ProductUpdateSerializer,
    }
    permission_action_map = {
        "create": [IsSuperUser],
        "list": [AllowAny],
        "retrieve": [AllowAny],
        "partial_update": [IsSuperUser],
        "destroy": [IsSuperUser],
    }
    parser_classes = [JSONParser, MultiPartParser]
    http_method_names = ["get", "post", "patch", "delete"]
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
        return product_repository.get_by_slug(slug, active=True)

    @openapi.create_product
    @inject
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        serializer = ProductListSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @openapi.update_product
    def partial_update(
        self, request, *args,
        product_repository: ProductRepository = Provide[Container.product_package.product_repository],
        **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        slug = kwargs["slug"]
        product = product_repository.update_product(slug, **serializer.validated_data)
        serializer = ProductListSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @openapi.delete_product
    def destroy(self, request, *args, **kwargs):
        return super(ProductViewSet, self).destroy(request, *args, **kwargs)


    @openapi.list_products
    def list(self, request, *args, **kwargs):
        return super(ProductViewSet, self).list(request, *args, **kwargs)

    @openapi.info_product
    def retrieve(self, request, *args, **kwargs):
        product = self.get_object(**kwargs)
        serializer = self.get_serializer(product)
        return Response(serializer.data)


