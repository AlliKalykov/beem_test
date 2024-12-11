from abc_back.api.openapi import extend_schema

from .serializers import CartItemShortSerializer


add_to_cart = extend_schema(
    summary="Добавление в корзину.",
    description="Добавление в корзину.",
    responses={
        201: CartItemShortSerializer,
        400: None,
        401: None,
    },
)
