from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from django.db import models


if TYPE_CHECKING:
    from abc_back.products.repositories import ProductRepository


class ActiveProductManager(models.Manager):
    """Менеджер модели для работы с активными пользователями."""

    @inject
    def get_queryset(self, product_repository: ProductRepository = Provide["product_package.product_repository"]):
        return product_repository.get_active()