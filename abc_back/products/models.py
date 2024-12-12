from django.db import models

from abc_back.mixins import PublishedModelMixin, TimestampedModelMixin
from abc_back.utils import generate_filename

from .constants import SizeType
from .managers import ActiveProductManager, ActiveSubProductManager


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


def brand_logo_upload_to(instance, filename) -> str:
    new_filename = generate_filename(filename)
    return f"{BASE_PRODUCTS_MEDIA_FOLDER}/brand/logo/{new_filename}"


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
    slug = models.SlugField("Слаг", db_index=True, unique=True, max_length=255, help_text="Короткое название для URL")

    objects = models.Manager()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """Возвращает абсолютный URL для категории."""
        from django.urls import reverse
        return reverse("category_detail", kwargs={"slug": self.slug})

    def get_children(self):
        """Возвращает дочерние категории."""
        return self.children.filter(is_active=True)

    def is_root(self):
        """Проверяет, является ли категория корневой."""
        return self.parent is None

    def get_category_line(self):
        root = self
        category_line = [root]
        while root.parent:
            root = root.parent
            category_line.append(root)
        return category_line


class Brand(PublishedModelMixin):

    name = models.CharField("Название", max_length=255, unique=True, db_index=True)
    slug = models.SlugField("Слаг", max_length=255, unique=True, help_text="Короткое название для URL")
    logo = models.FileField("Логотип", upload_to=brand_logo_upload_to, blank=True, null=True)
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

    category = models.ManyToManyField(
        Category, verbose_name="Категория",
        related_name="products", related_query_name="product",
    )
    brand = models.ForeignKey(
        Brand, verbose_name="Бренд", on_delete=models.CASCADE,
        related_name="products", related_query_name="product",
    )

    is_novelty = models.BooleanField("Новинка", default=False, help_text="Товар является новинкой")
    is_bestseller = models.BooleanField("Бестселлер", default=False, help_text="Товар является бестселлером")
    is_back_in_stock = models.BooleanField("В наличии", default=False, help_text="Товар вернулся в наличии")
    is_recommendation = models.BooleanField(
        "Рекомендация", default=False, help_text="Товар является рекомендацией магазина",
    )

    is_active = models.BooleanField("Активность", default=True)

    description = models.TextField("Описание", blank=True, null=True)
    use = models.TextField("Применение/Использование", blank=True, null=True)
    ingredient = models.TextField("Состав", blank=True, null=True)
    additional = models.TextField("Дополнение", blank=True, null=True)

    objects = models.Manager()
    active = ActiveProductManager()

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name}"

    @property
    def categories(self):
        return [
            category.get_category_line() for category in self.category.all()
        ]


class ProductPoster(TimestampedModelMixin, PublishedModelMixin):
    product = models.ForeignKey(
        Product, verbose_name="Товар", on_delete=models.CASCADE,
        related_name="posters", related_query_name="poster",
    )
    image = models.ImageField("Изображение", upload_to=product_image_upload_to)
    is_featured = models.BooleanField("Основное изображение", default=False)

    class Meta:
        verbose_name = "Постер"
        verbose_name_plural = "Постеры"

    def __str__(self):
        return f"[{self.id}]: {self.product}"


class Color(models.Model):

    name = models.CharField("Цвет", max_length=24, unique=True)
    hex_code = models.CharField("Шестнадцатеричный код", max_length=24, unique=True)
    description = models.TextField("Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    def __str__(self):
        return f"{self.name}"


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

    stock = models.PositiveIntegerField("В наличии", default=0)
    is_available = models.BooleanField("Доступен для продажи", default=True)

    article = models.PositiveIntegerField("Артикул", unique=True)
    sell_price = models.FloatField("Цена продажи", default=0)
    purchase_price = models.FloatField("Цена закупки", default=0)
    sale_percent = models.PositiveIntegerField("Процент скидки", default=0)
    final_price = models.FloatField("Конечная цена", default=0)

    production_date = models.DateField("Дата производства", null=True, blank=True)
    expiration_date = models.DateField("Срок годности", null=True, blank=True)
    shelf_life = models.PositiveIntegerField("Срок хранения", null=True, blank=True)

    objects = models.Manager()
    active = ActiveSubProductManager()

    class Meta:
        verbose_name = "Подтовар"
        verbose_name_plural = "Подтовары"

    def __str__(self):
        return f"{self.product.name} {self.size} {self.color}"

    def save(self, *args, **kwargs):
        if self.sale_percent and self.sell_price:
            self.final_price = self.sell_price - (self.sell_price * self.sale_percent / 100)
        else:
            self.final_price = self.sell_price
        super().save(*args, **kwargs)


class SubProductImage(models.Model):
    sub_product = models.ForeignKey(
        SubProduct, verbose_name="Подтовар", on_delete=models.CASCADE, null=True,
        related_name="posters", related_query_name="poster",
    )
    image = models.ImageField("Изображение", upload_to=sub_product_image_upload_to)
    is_featured = models.BooleanField("Основное изображение", default=False)

    class Meta:
        verbose_name = "Изображение подпродукта"
        verbose_name_plural = "Изображения подпродуктов"

    def __str__(self):
        return f"{self.image}"
