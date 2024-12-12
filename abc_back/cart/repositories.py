from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import DecimalField, ExpressionWrapper, F, Prefetch, QuerySet, Sum

from abc_back.cart.models import Cart, CartItem
from abc_back.exceptions import NotFoundError
from abc_back.types import Id
from abc_back.users.models import User

if TYPE_CHECKING:
    from abc_back.products.models import  SubProduct


class CartRepository:
    """Репозиторий для работы с корзиной."""

    def get_cart(self, user_id: Id | None = None, session_key: str | None = None) -> Cart | None:
        cart = self.get_cart_by_user_id(user_id) if user_id else self.get_cart_by_session_key(session_key)
        return cart

    def get_cart_with_calculations(self, user_id: Id | None = None, session_key: str | None = None) -> Cart | None:
        cart = self.get_cart(user_id, session_key)
        if cart:
            cart_items_with_cost_calculations = self.get_cart_items(cart.id)

            # Вычисление общих сумм
            total_amount = cart_items_with_cost_calculations.aggregate(
                total_amount=Sum("total_price"),
                total_amount_without_sale=Sum("amount_without_sale"),
                total_sale_amount=Sum("sale_amount"),
            )

            cart.total_amount = total_amount["total_amount"] or 0
            cart.total_amount_without_sale = total_amount["total_amount_without_sale"] or 0
            cart.total_sale_amount = total_amount["total_sale_amount"] or 0

            return cart
        else:
            raise NotFoundError("Корзина не найдена")

    def get_cart_by_user_id(self, user_id: Id) -> Cart | None:
        try:
            cart = Cart.objects.get(user_id=user_id).prefetch_related("items")
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
        cart = self.get_cart(user_id, session_key)
        if not cart:
            cart = self.create_cart(user_id, session_key)
        return cart

    def delete_cart(self, cart):
        cart.delete()

    def clear_cart(self, cart):
        cart.items.all().delete()

    def get_or_create_item(self, cart: Cart, sub_product: SubProduct, quantity: int) -> CartItem:
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            sub_product=sub_product,
            defaults={"quantity": quantity},
        )
        return self.get_cart_items(item.id)

    def get_cart_items(self, cart_id: id) -> QuerySet[CartItem]:
        cart_items_with_cost_calculations = (
            CartItem.objects.filter(cart_id=cart_id)
            .prefetch_related("sub_product")
            .annotate(
                sell_price=F("sub_product__sell_price"),
                sale_percent=F("sub_product__sale_percent"),
                final_price=F("sub_product__final_price"),
                amount_without_sale=ExpressionWrapper(
                    F("quantity") * F("sub_product__sell_price"),
                    output_field=DecimalField(decimal_places=2, max_digits=10),
                ),
                sale_amount=ExpressionWrapper(
                    F("quantity") * F("sub_product__sell_price") * F("sub_product__sale_percent") / 100,
                    output_field=DecimalField(decimal_places=2, max_digits=10),
                ),
                total_price=ExpressionWrapper(
                    F("quantity") * F("sub_product__final_price"),
                    output_field=DecimalField(decimal_places=2, max_digits=10),
                ),
            )
        )
        return cart_items_with_cost_calculations

    def get_cart_item_by_id(self, cart_item_id: Id) -> CartItem | None:
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return None
        return cart_item
