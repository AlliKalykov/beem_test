from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from django.db.models import BooleanField, Case, Prefetch, QuerySet, Value, When

from abc_back.exceptions import NotFoundError
from abc_back.types import Id

from .models import Category, Product
from abc_back.favorites.models import FavoriteProduct


if TYPE_CHECKING:
    from abc_back.users.models import User


class ProductRepository:
    """Репозиторий для работы с данными пользователей."""

    def get_active(self, user: Optional[User] = None) -> QuerySet[Product]:
        """Получение активных товаров с лайками, избранными и их количествами."""
        is_user_authenticated = user and user.is_authenticated
        favorite_qs = (
            FavoriteProduct.objects.filter(user=user) if is_user_authenticated else FavoriteProduct.objects.none()
        )
        products = (
            Product.objects.filter(is_active=True)
            .annotate(
                is_favorite=Case(
                    When(favorite__in=favorite_qs, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
            .prefetch_related(Prefetch("favorites", queryset=favorite_qs))
        )
        return products

    def get_by_pk(self, product_pk: Id, /, *, active: bool = False) -> Product:
        """Получение пользователя по ID."""
        base_manager = Product.active if active else Product.objects
        try:
            product = base_manager.get(pk=product_pk)
        except Product.DoesNotExist:
            raise NotFoundError
        return product

    def get_by_pks(self, product_pks: list[Id], /, *, active: bool = False) -> QuerySet[Product]:
        """Получение пользователей по списку ID."""
        base_manager = Product.active if active else Product.objects
        return base_manager.filter(pk__in=product_pks)

    def get_by_slug(self, slug: str, /, *, active: bool = False) -> Product:
        """Получение пользователя по почте."""
        base_manager = Product.active if active else Product.objects
        try:
            product = base_manager.get(slug=slug)
        except Product.DoesNotExist:
            raise NotFoundError
        return product

    def update_product(self, slug: str, **kwargs):
        category = kwargs.pop("category")
        product = Product.objects.get(slug=slug)
        if category:
            product.category.set(category)
        product.save(**kwargs)
        return product


class CategoryRepository:
    """Репозиторий для работы с данными пользователей."""

    def get_by_pk(self, category_pk: Id) -> Category:
        """Получение пользователя по ID."""
        try:
            category = Category.objects.get(pk=category_pk).prefetch_related("children")
        except Category.DoesNotExist:
            raise NotFoundError
        return category

    def get_by_pks(self, category_pks: list[Id]) -> QuerySet[Category]:
        """Получение пользователей по списку ID."""
        return Category.objects.filter(pk__in=category_pks)

    def get_by_slug(self, slug: str) -> Category:
        """Получение пользователя по почте."""
        try:
            category = Category.objects.get(slug=slug).prefetch_related("children")
        except Category.DoesNotExist:
            raise NotFoundError
        return category

    def get_featured(self) -> QuerySet[Category]:
        return Category.objects.filter(is_featured=True).prefetch_related("children")

    def get_all(self) -> QuerySet[Category]:
        return Category.objects.all()
