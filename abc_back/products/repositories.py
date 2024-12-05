from django.db.models import QuerySet

from abc_back.exceptions import NotFoundError
from abc_back.products.models import Category, Product
from abc_back.types import Id


class ProductRepository:
    """Репозиторий для работы с данными пользователей."""

    def get_active(self) -> QuerySet[Product]:
        """Получение активных пользователей."""
        return Product.objects.filter(is_active=True)

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
