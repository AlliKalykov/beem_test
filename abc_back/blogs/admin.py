from __future__ import annotations

from django.contrib import admin

from abc_back.blogs.models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name", "slug")
    search_fields = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug")
    list_display_links = ("id", "title", "slug")
    search_fields = ("id", "title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories", "authors", "related_post", "related_product")
