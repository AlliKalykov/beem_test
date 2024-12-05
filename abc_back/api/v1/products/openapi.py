from abc_back.api.openapi import extend_schema

from .serializers import CategoryTreeSerializer, ProductShortSerializer, ParentCategorySerializer, ProductListSerializer


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
        200: ProductListSerializer,
        400: None,
        401: None,
    },
)

create_product = extend_schema(
    summary="Создание продукта.",
    description="Создание продукта.",
    responses={
        201: ProductListSerializer,
        400: None,
        401: None,
    },
)

update_product = extend_schema(
    summary="Обновление продукта.",
    description="Обновление продукта.",
    responses={
        200: ProductListSerializer,
        400: None,
        401: None,
    },
)

delete_product = extend_schema(
    summary="Удаление продукта.",
    description="Удаление продукта.",
    responses={
        200: None,
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

create_category = extend_schema(
    summary="Создание категории.",
    description="Создание категории.",
    responses={
        201: ParentCategorySerializer,
        400: None,
    },
)

update_category = extend_schema(
    summary="Обновление категории.",
    description="Обновление категории.",
    responses={
        200: ParentCategorySerializer,
        400: None,
    },
)

delete_category = extend_schema(
    summary="Удаление категории продукта.",
    description="Удаление категории продукта.",
    responses={
        200: None,
        400: None,
    },
)
