from __future__ import annotations

from django.contrib import admin

from abc_back.blogs.models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_display_links = ("title",)
    search_fields = ("title",)
