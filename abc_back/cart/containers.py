from __future__ import annotations

from dependency_injector import containers, providers

from abc_back.products.repositories import SubProductRepository

from .repositories import CartRepository
from .services import CartService


class CartContainer(containers.DeclarativeContainer):
    cart_repository = providers.Factory(CartRepository)
    sub_product_repository = providers.Singleton(SubProductRepository)
    cart_service = providers.Factory(
        CartService,
        cart_repository=cart_repository,
        sub_product_repository=sub_product_repository,
    )
