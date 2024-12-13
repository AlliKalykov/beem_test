from django.contrib import admin

from abc_back.mixins import ReadOnlyAdminMixin
from abc_back.utils import render_object_changelist_link

from .models import Cart, CartItem


# TODO: добавить перед PROD ReadOnlyAdminMixin,
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session_key", "created_at", "cart_items_link")
    list_display_links = ("id", "user", "session_key")
    list_filter = ("created_at",)
    search_fields = ("user", "user__email", "session_key")

    inlines = [CartItemInline]

    @admin.display(description="Товары в корзине")
    def cart_items_link(self, obj):
        """Добавляет ссылку на OrderItemAdmin с фильтром по текущему заказу."""
        if not obj.items.exists():
            return f"Пустая корзина"
        return render_object_changelist_link(
            obj.items.first(), content="Товары в корзине", query=f"cart__id__exact={obj.pk}", new_tab=True,
        )


@admin.register(CartItem)
class CartItemAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("id", "cart", "sub_product", "quantity")
    list_display_links = ("id", "cart")
    search_fields = ("cart",)
    list_filter = ("created_at",)
