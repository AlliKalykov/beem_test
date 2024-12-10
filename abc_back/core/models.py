from __future__ import annotations

from django.db import models

from abc_back.mixins import SortableModelMixin


class Country(SortableModelMixin):
    name = models.CharField("Страна", max_length=36, unique=True)
    slug = models.SlugField("Слаг", max_length=36, unique=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = ["position"]

    def __str__(self):
        return f"{self.name}"


class City(SortableModelMixin):
    country = models.ForeignKey(
        Country, verbose_name="Страна", on_delete=models.CASCADE,
        related_name="cities", related_query_name="city",
    )
    name = models.CharField("Город", max_length=36, unique=True)
    slug = models.SlugField("Слаг", max_length=36, unique=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ["position"]

    def __str__(self):
        return f"{self.country} {self.name}"
