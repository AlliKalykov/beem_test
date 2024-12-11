from __future__ import annotations

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from abc_back.core.models import City
from abc_back.mixins import TimestampedModelMixin
from abc_back.products.models import SubProduct
from abc_back.users.models import User

from .constants import OrderStatus


class Order(TimestampedModelMixin):
    user = models.ForeignKey(
        User, verbose_name="Пользователь", blank=True, null=True, on_delete=models.SET_NULL,
        related_name="orders", related_query_name="order",
    )

    fio = models.CharField("ФИО", max_length=255)
    email = models.EmailField("Электронная почта")
    phone = PhoneNumberField("Номер телефона")

    city = models.ForeignKey(
        City, verbose_name="Город", on_delete=models.PROTECT,
        related_name="orders", related_query_name="order",
    )
    street = models.CharField("Улица", max_length=255)
    house = models.CharField("Дом", max_length=255)
    additional = models.CharField("Дополнение", max_length=255, blank=True, null=True)

    total_amount = models.DecimalField("Общая сумма", max_digits=10, decimal_places=2, blank=True, null=True)
    sale_percent = models.DecimalField("Скидка", max_digits=10, decimal_places=2, blank=True, null=True)
    amount_with_sale = models.DecimalField(
        "Сумма с учетом скидки", max_digits=10, decimal_places=2, blank=True, null=True,
    )
    delivery_amount = models.DecimalField("Сумма доставки", max_digits=10, decimal_places=2, blank=True, null=True)
    final_amount = models.DecimalField("Итоговая сумма", max_digits=10, decimal_places=2, blank=True, null=True)

    status = models.CharField(
        "Статус", max_length=24, choices=OrderStatus.choices, default=OrderStatus.DRAFT,
    )
    session_key = models.CharField("Сессия", max_length=255, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"[{self.id}]: {self.email}"


class OrderItem(TimestampedModelMixin):
    order = models.ForeignKey(
        Order, verbose_name="Заказ", on_delete=models.CASCADE,
        related_name="items", related_query_name="item",
    )

    sub_product = models.ForeignKey(
        SubProduct, verbose_name="Товар", on_delete=models.CASCADE,
        related_name="order_items", related_query_name="order_item",
    )
    quantity = models.PositiveIntegerField("Количество")

    sell_price = models.FloatField("Цена продажи", blank=True, null=True)
    sale_percent = models.PositiveIntegerField("Процент скидки", blank=True, null=True)
    final_price = models.FloatField("Конечная цена", blank=True, null=True)

    total_sum = models.FloatField("Итоговая сумма", blank=True, null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"[{self.id}]: [{self.order.id}] - {self.order.email}"
