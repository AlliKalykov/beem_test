from abc_back.api.openapi import extend_schema

from .serializers import ProductSerializer


list_products = extend_schema(
    summary="Список продуктов.",
    description="Получение списка продуктов.",
    responses={
        200: ProductSerializer(many=True),
        400: None,
        401: None,
    },
)

info_product = extend_schema(
    summary="Получение продукта.",
    description="Получение продукта.",
    responses={
        200: ProductSerializer,
        400: None,
        401: None,
    },
)
