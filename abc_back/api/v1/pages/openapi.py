from abc_back.api.openapi import extend_schema

from .serializers import AboutUsSerializer


about_us = extend_schema(
    summary="О нас.",
    description="Получение информации о нас.",
    responses={
        200: AboutUsSerializer,
        400: None,
        401: None,
    },
)
