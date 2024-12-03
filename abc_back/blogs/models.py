from django.db import models

from abc_back.users.models import User
from abc_back.products.models import Product

class Category(models.Model):
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField("Слаг", max_length=255, unique=True, help_text="Короткое название для URL")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"

    def __str__(self):
        return self.name


class Post(models.Model):
    slug = models.SlugField("Слаг", max_length=255, unique=True, help_text="Короткое название для URL")
    title = models.TextField("Заголовок")
    text = models.TextField("Текст")
    poster = models.FileField("Постер")
    categories = models.ManyToManyField(Category, verbose_name="Категории")
    authors = models.ManyToManyField(User, verbose_name="Автор")
    is_active = models.BooleanField("Активность")
    related_post = models.ManyToManyField("self", verbose_name="Родитель", null=True, blank=True)
    related_product = models.ManyToManyField(Product, verbose_name="Связанный продукт")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пост"

    def __str__(self):
        return self.title
