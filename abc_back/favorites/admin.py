from django.contrib import admin

from .models import FavoriteProduct


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "user")
    list_display_links = ("id", "product", "user")
    search_fields = ("product", "user")
    ordering = ("product", "user")
