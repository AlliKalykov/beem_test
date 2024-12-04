from django.db import models

from abc_back.products.models import Product
from abc_back.users.models import User
from abc_back.utils import generate_filename


BASE_BLOGS_MEDIA_FOLDER = "blogs"


def post_file_upload_to(instance, filename):
    new_filename = generate_filename(filename)
    return f"{BASE_BLOGS_MEDIA_FOLDER}/post/{new_filename}"


class Category(models.Model):
    name = models.CharField("Название", max_length=255)
    slug = models.SlugField("Слаг", max_length=255, unique=True, help_text="Короткое название для URL")

    objects = models.Manager()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"

    def __str__(self):
        return self.name


class Post(models.Model):
    slug = models.SlugField("Слаг", max_length=255, unique=True, help_text="Короткое название для URL")
    title = models.TextField("Заголовок")
    text = models.TextField("Текст")
    poster = models.FileField("Постер", upload_to=post_file_upload_to, blank=True, null=True)
    categories = models.ManyToManyField(
        Category, verbose_name="Категории", related_name="posts", related_query_name="post",
    )
    authors = models.ManyToManyField(User, verbose_name="Автор")
    is_active = models.BooleanField("Активность")
    related_post = models.ManyToManyField("self", verbose_name="Родитель", null=True, blank=True)
    related_product = models.ManyToManyField(
        Product, verbose_name="Связанный продукт", null=True, blank=True,
        related_name="posts", related_query_name="post",
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пост"

    def __str__(self):
        return self.title
