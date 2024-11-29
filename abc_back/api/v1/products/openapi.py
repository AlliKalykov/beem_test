from abc_back.api.openapi import extend_schema

from .serializers import CategoryTreeSerializer, ProductShortSerializer


list_products = extend_schema(
    summary="Список продуктов.",
    description="Получение списка продуктов.",
    responses={
        200: ProductShortSerializer(many=True),
        400: None,
        401: None,
    },
)

info_product = extend_schema(
    summary="Получение продукта.",
    description="Получение продукта.",
    responses={
        200: ProductShortSerializer,
        400: None,
        401: None,
    },
)

list_categories = extend_schema(
    summary="Список категорий.",
    description="Получение списка категорий.",
    responses={
        200: CategoryTreeSerializer(many=True),
        400: None,
    },
)

info_category = extend_schema(
    summary="Получение категории.",
    description="Получение категории.",
    responses={
        200: CategoryTreeSerializer,
        400: None,
    },
)
