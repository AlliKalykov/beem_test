from django.core.exceptions import ValidationError
from django.db import models

from abc_back.mixins import PublishedModelMixin, TimestampedModelMixin
from abc_back.products.models import Product
from abc_back.users.models import User
from abc_back.utils import generate_filename


def favorite_review_image_upload_to(instance, filename) -> str:
    new_filename = generate_filename(filename)
    return f"reviews/{new_filename}"


class FavoriteReview(TimestampedModelMixin, PublishedModelMixin):
    product = models.ForeignKey(
        Product, verbose_name="Продукт", on_delete=models.CASCADE,
        related_name="favorite_reviews", related_query_name="favorite_review",
    )
    image = models.ImageField("Изображение", upload_to=favorite_review_image_upload_to)

    objects = models.Manager()

    class Meta:
        verbose_name = "Статичные отзыв"
        verbose_name_plural = "Статичные отзывы"

    def __str__(self):
        return f"{self.product}"


class Review(TimestampedModelMixin, PublishedModelMixin):
    product = models.ForeignKey(
        Product, verbose_name="Продукт", on_delete=models.CASCADE,
        related_name="reviews", related_query_name="review",
    )
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE,
        related_name="reviews", related_query_name="review",
    )
    rate = models.PositiveSmallIntegerField("Рейтинг", default=0)
    comment = models.TextField("Комментарии")
    image = models.ImageField("Изображение", upload_to=favorite_review_image_upload_to, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.product} - {self.user}"

    def clean(self):
        if 0 <= self.rate <= 5:
            super().clean()
        else:
            raise ValidationError("Рейтинг должен быть от 0 до 5")


class Like(TimestampedModelMixin, PublishedModelMixin):
    review = models.ForeignKey(
        Review, verbose_name="Отзыв", on_delete=models.CASCADE,
        related_name="likes", related_query_name="like",
    )
    user = models.ForeignKey(
        User, verbose_name="Пользователь", on_delete=models.CASCADE,
        related_name="likes", related_query_name="like",
    )
    liked = models.BooleanField("Лайк", default=False)

    objects = models.Manager()

    class Meta:
        verbose_name = "Лайк отзыва"
        verbose_name_plural = "Лайки отзывов"
        unique_together = ("review", "user")

    def __str__(self):
        return f"{self.review} - {self.user}"
