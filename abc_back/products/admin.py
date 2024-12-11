from django.contrib import admin

from abc_back.mixins import ReadOnlyAdminMixin
from abc_back.products.models import Brand, Category, Color, Product, Size, SubProduct, SubProductImage
from abc_back.utils import render_object_changelist_link


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
    list_display = ("name", "slug", "is_published", "is_featured")
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
    list_display = ("id", "name", "slug", "get_categories", "brand", "get_sub_products_link")
    list_display_links = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("category", "brand", "created_at")

    filter_horizontal = ("category",)
    inlines = [SubProductInline]

    @admin.display(description="Категории")
    def get_categories(self, obj):
        categories = obj.category.values_list("name", flat=True)
        return f"{', '.join(categories)}"

    @admin.display(description="Позиции товара")
    def get_sub_products_link(self, obj):
        sub_product_count = obj.sub_products.count()
        return render_object_changelist_link(
            SubProduct.objects.first(), content=f"Позиции товара ({sub_product_count})",
            query=f"product__id__exact={obj.pk}", new_tab=True,
        )


@admin.register(SubProduct)
class SubProductAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("id", "slug", "product", "stock", "size", "color", "sale_percent", "final_price", "is_available")
    list_display_links = ("id", "slug", "product")
    search_fields = ("id", "slug", "product")
    list_filter = ("is_available", "production_date", "expiration_date", "created_at")
