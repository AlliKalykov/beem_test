from __future__ import annotations

from abc_back.products.repositories import SubProductRepository
from abc_back.types import Id

from ..api.exceptions import BadRequest
from .models import CartItem
from .repositories import CartRepository


class CartService:
    """Сервис для работы с пользователями."""

    def __init__(
        self,
        cart_repository: CartRepository,
        sub_product_repository: SubProductRepository,
    ) -> None:
        self._cart_repository = cart_repository
        self._sub_product_repository = sub_product_repository

    def add_item(self, user_id: Id, session_key: str, sub_product_id: Id, quantity: int) -> CartItem:
        cart = self._cart_repository.get_or_create_cart(user_id, session_key)
        sub_product = self._sub_product_repository.get_by_pk(sub_product_id, active=True)
        if CartItem.objects.filter(cart=cart, sub_product=sub_product).exists():
            raise BadRequest("Товар уже в корзине")
        if quantity > sub_product.stock:
            raise BadRequest("Недостаточно товара в наличии")
        cart_item= self._cart_repository.get_or_create_item(cart, sub_product, quantity)
        return cart_item

    def change_item_quantity(self, user_id: Id, session_key: str, item_id: Id, quantity: int):
        cart = self._cart_repository.get_or_create_cart(user_id, session_key)
        item = self._cart_repository.get_cart_item_by_id(cart.id, item_id)
        if item.cart != cart:
            raise BadRequest("Товар не в корзине")
        if quantity > item.sub_product.stock:
            raise BadRequest("Недостаточно товара в наличии")
        item.quantity = quantity
        item.save()
        return item

    def remove_item(self, user_id: Id, session_key: str, item_id: Id):
        cart = self._cart_repository.get_or_create_cart(user_id, session_key)
        item = self._cart_repository.get_cart_item_by_id(cart.id, item_id)
        if item.cart != cart:
            raise BadRequest("Товар не в корзине")
        item.delete()

    def get_or_create_cart(self, user_id: Id | None = None, session_key: str | None = None):
        return self._cart_repository.get_or_create_cart(user_id, session_key)

    def clear_cart(self, user_id: Id | None = None, session_key: str | None = None):
        cart = (
            self._cart_repository.get_cart_by_user_id(user_id) if user_id else
            self._cart_repository.get_cart_by_session_key(session_key)
        )
        if cart:
            self._cart_repository.clear_cart(cart)
