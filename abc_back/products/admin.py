from django.contrib import admin

from abc_back.products.models import Brand, Category, Color, Product, Size, SubProduct, SubProductImage


class SubProductImageInline(admin.TabularInline):
    model = SubProductImage
    extra = 0


class SubProductInline(admin.TabularInline):
    model = SubProduct
    extra = 0
    inlines = [SubProductImageInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "description")
    list_display_links = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_featured")
    list_display_links = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_code", "description")
    list_display_links = ("name",)
    search_fields = ("name", "hex_code")


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("kind", "value", "description")
    list_display_links = ("kind", "value")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "get_categories", "brand")
    list_display_links = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    filter_horizontal = ("category",)
    inlines = [SubProductInline]

    @admin.display(description="Категории")
    def get_categories(self, obj):
        categories = obj.category.values_list("name", flat=True)
        return f"{', '.join(categories)}"
