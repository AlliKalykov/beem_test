from django.db import models

from abc_back.mixins import TimestampedModelMixin
from abc_back.products.models import Product
from abc_back.users.models import User


class FavoriteProduct(TimestampedModelMixin):
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE,
        related_name="favorites", related_query_name="favorite",
    )
    product = models.ForeignKey(
        Product, verbose_name="Продукт", on_delete=models.CASCADE,
        related_name="favorites", related_query_name="favorite",
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.product} - {self.user}"
