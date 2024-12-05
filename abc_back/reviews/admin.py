from django.contrib import admin

from .models import FavoriteReview, Like, Review


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0


@admin.register(FavoriteReview)
class FavoriteReviewAdmin(admin.ModelAdmin):
    list_display = ("product",)
    search_fields = ("product",)
    ordering = ("product",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product",)
    search_fields = ("product",)
    ordering = ("product",)

    inlines = [LikeInline]
