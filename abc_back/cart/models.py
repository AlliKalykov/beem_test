from __future__ import annotations

from django.db import models

from abc_back.mixins import TimestampedModelMixin
from abc_back.products.models import SubProduct
from abc_back.users.models import User


class Cart(TimestampedModelMixin):
    user = models.ForeignKey(User, verbose_name="Пользователь", blank=True, null=True, on_delete=models.SET_NULL)
    session_key = models.CharField("Сессия", max_length=255)

    objects = models.Manager()

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        if self.user:
            return f"[{self.id}] {self.user}"
        return f"[{self.id}] {self.session_key}"


class CartItem(TimestampedModelMixin):

    cart = models.ForeignKey(
        Cart, verbose_name="Корзина", on_delete=models.CASCADE,
        related_name="items", related_query_name="item",
    )
    sub_product = models.ForeignKey(
        SubProduct, verbose_name="Товар", on_delete=models.CASCADE,
        related_name="cart_items", related_query_name="cart_item",
    )
    quantity = models.PositiveIntegerField("Количество", default=1)

    objects = models.Manager()

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"
        unique_together = ("cart", "sub_product")

    def __str__(self):
        return f"[{self.id}] {self.cart} - {self.sub_product}"