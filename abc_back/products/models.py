from django.db import models

from abc_back.mixins import PublishedModelMixin, TimestampedModelMixin
from abc_back.utils import generate_filename

from .constants import SizeType


BASE_PRODUCTS_MEDIA_FOLDER = "products"


def product_image_upload_to(instance, filename) -> str:
    new_filename = generate_filename(filename)
    return f"{BASE_PRODUCTS_MEDIA_FOLDER}/product/images/{new_filename}"


def product_file_upload_to(instance, filename) -> str:
    new_filename = generate_filename(filename)
    return f"{BASE_PRODUCTS_MEDIA_FOLDER}/prodict/files/{new_filename}"


def sub_product_image_upload_to(instance, filename) -> str:
    new_filename = generate_filename(filename)
    return f"{BASE_PRODUCTS_MEDIA_FOLDER}/sub_product/images/{new_filename}"


class Category(PublishedModelMixin):

    is_featured = models.BooleanField(
        "Главная категория", default=False,
        help_text="При выборе данной опции, категория будет отображаться на главном меню",
    )
    parent = models.ForeignKey(
        "self", verbose_name="Родитель", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="children", related_query_name="child",
        help_text="Если категория является подкатегорией, выберите родительскую категорию",
    )
    name = models.CharField("Название", max_length=255, unique=True, db_index=True)
    slug = models.SlugField("Слаг", max_length=255, unique=True, help_text="Короткое название для URL")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"


class Brand(PublishedModelMixin):

    name = models.CharField("Название", max_length=255, unique=True, db_index=True)
    slug = models.SlugField("Слаг", max_length=255, unique=True, help_text="Короткое название для URL")
    description = models.TextField("Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def __str__(self):
        return f"{self.name}"


class Product(TimestampedModelMixin, PublishedModelMixin):
    """Товар - Сущность, представляющая товар в магазине."""

    name = models.CharField("Название", max_length=255, unique=True, db_index=True)
    slug = models.SlugField("Слаг", max_length=255, unique=True, help_text="Короткое название для URL")
    poster = models.FileField("Постер", upload_to=product_image_upload_to, blank=True, null=True)

    category = models.ManyToManyField(
        Category, verbose_name="Категория",
        related_name="products", related_query_name="product",
    )
    brand = models.ForeignKey(Brand, verbose_name="Бренд", on_delete=models.CASCADE)

    is_novelty = models.BooleanField("Новинка", default=False, help_text="Товар является новинкой")
    is_bestseller = models.BooleanField("Бестселлер", default=False, help_text="Товар является бестселлером")
    is_back_in_stock = models.BooleanField("В наличии", default=False, help_text="Товар вернулся в наличии")
    is_recommendation = models.BooleanField(
        "Рекомендация", default=False, help_text="Товар является рекомендацией магазина",
    )

    description = models.TextField("Описание", blank=True, null=True)
    use = models.TextField("Применение/Использование", blank=True, null=True)
    ingredient = models.TextField("Состав", blank=True, null=True)
    additional = models.TextField("Дополнение", blank=True, null=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name}"


class Color(models.Model):

    color = models.CharField("Цвет", max_length=24, unique=True)
    description = models.TextField("Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    def __str__(self):
        return f"{self.color}"


class Size(models.Model):

    kind = models.CharField("Тип", max_length=24, choices=SizeType.choices)
    value = models.PositiveIntegerField("Значение")
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("kind", "value")
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self):
        return f"{self.value} {self.kind}"


class SubProductImage(models.Model):
    image = models.ImageField("Изображение", upload_to=sub_product_image_upload_to)
    is_featured = models.BooleanField("Основное изображение", default=False)

    class Meta:
        verbose_name = "Изображение подпродукта"
        verbose_name_plural = "Изображения подпродуктов"

    def __str__(self):
        return f"{self.image}"


class SubProduct(TimestampedModelMixin, PublishedModelMixin):
    """Подтовар - Сущность, представляющая товар со всеми размерами и цветами.

    Пример:
    Товар: "VERSACE"
        Подтовары:
        - "VERSACE 20 gr red", "VERSACE 20 gr black", "VERSACE 20 gr blue"
        - "VERSACE 30 gr red", "VERSACE 30 gr black", "VERSACE 30 gr blue"
        - "VERSACE 40 gr red", "VERSACE 40 gr black", "VERSACE 40 gr blue"
    """

    product = models.ForeignKey(
        Product, verbose_name="Товар", on_delete=models.PROTECT,
        related_name="sub_products", related_query_name="sub_product",
    )
    size = models.ForeignKey(
        Size, verbose_name="Размер", on_delete=models.CASCADE,
        related_name="sub_products", related_query_name="sub_product",
    )
    color = models.ForeignKey(
        Color, verbose_name="Цвет", on_delete=models.CASCADE,
        related_name="sub_products", related_query_name="sub_product",
    )

    slug = models.SlugField("Слаг", max_length=255, unique=True, help_text="Короткое название для URL")

    posters = models.ManyToManyField(
        SubProductImage, verbose_name="Изображение подпродукта", blank=True,
        related_name="sub_products", related_query_name="sub_product",
    )

    stock = models.PositiveIntegerField("В наличии", default=0)
    is_available = models.BooleanField("Доступен для продажи", default=True)

    article = models.PositiveIntegerField("Артикул", unique=True)
    sell_price = models.FloatField("Цена продажи", default=0)
    purchase_price = models.FloatField("Цена закупки", default=0)
    sale_percent = models.PositiveIntegerField("Процент скидки", default=0)
    final_price = models.FloatField("Цена продажи", default=0)

    production_date = models.DateField("Дата производства", null=True, blank=True)
    expiration_date = models.DateField("Срок годности", null=True, blank=True)
    shelf_life = models.PositiveIntegerField("Срок хранения", null=True, blank=True)

    class Meta:
        verbose_name = "Подтовар"
        verbose_name_plural = "Подтовары"

    def __str__(self):
        return f"{self.product.name} {self.size} {self.color}"

    def save(self, *args, **kwargs):
        if self.sale_percent and self.sell_price:
            self.final_price = self.sell_price - (self.sell_price * self.sale_percent / 100)
        super().save(*args, **kwargs)
