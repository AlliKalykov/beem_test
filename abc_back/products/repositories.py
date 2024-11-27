from django.db.models import QuerySet

from abc_back.exceptions import NotFoundError
from abc_back.products.models import Product
from abc_back.types import Id


class ProductRepository:
    """Репозиторий для работы с данными пользователей."""

    def get_active(self) -> QuerySet[Product]:
        """Получение активных пользователей."""
        return Product.objects.filter(is_active=True, tb_id__isnull=False)

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
