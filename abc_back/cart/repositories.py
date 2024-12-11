from __future__ import annotations

from django.db.models import QuerySet

from abc_back.cart.models import Cart, CartItem
from abc_back.exceptions import NotFoundError
from abc_back.types import Id
from abc_back.users.models import User


class CartRepository:
    """Репозиторий для работы с корзиной."""

    def get_cart_by_user_id(self, user_id: Id) -> Cart | None:
        try:
            cart = Cart.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None
        return cart

    def get_cart_by_session_key(self, session_key: str) -> Cart | None:
        try:
            cart = Cart.objects.get(session_key=session_key)
        except Cart.DoesNotExist:
            return None
        return cart

    def create_cart(self, user_id: Id | None = None, session_key=None):
        try:
            user = User.objects.get(id=user_id) if user_id else None
        except User.DoesNotExist:
            raise NotFoundError("Пользователь не найден")
        return Cart.objects.create(user=user, session_key=session_key)

    def get_or_create_cart(self, user_id: Id | None = None, session_key: str | None = None):
        cart = self.get_cart_by_user_id(user_id) if user_id else self.get_cart_by_session_key(session_key)
        if not cart:
            cart = self.create_cart(user_id, session_key)
        return cart

    def clear_cart(self, cart):
        cart.items.all().delete()

    def get_cart_items(self, cart: Cart) -> QuerySet[CartItem]:
        return cart.items.all()

    def get_cart_item_by_id(self, cart_item_id: Id) -> CartItem | None:
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return None
        return cart_item
