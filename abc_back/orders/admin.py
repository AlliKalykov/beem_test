from django.contrib import admin

from abc_back.mixins import ReadOnlyInlineMixin
from abc_back.utils import render_object_changelist_link

from .models import Order, OrderItem


# TODO: добавить перед PROD ReadOnlyInlineMixin,
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "user", "created_at", "status", "final_amount", "order_items_link")
    list_display_links = ("id", "email", "user")
    list_filter = ("created_at", "status")
    search_fields = ("fio", "email", "phone")

    inlines = [OrderItemInline]

    def order_items_link(self, obj):
        """Добавляет ссылку на OrderItemAdmin с фильтром по текущему заказу."""
        return render_object_changelist_link(
            obj.items.first(), content="Детали заказа", query=f"order__id__exact={obj.pk}", new_tab=True,
        )

    order_items_link.short_description = "Детали заказа"


@admin.register(OrderItem)
class OrderItemAdmin(ReadOnlyInlineMixin, admin.ModelAdmin):
    list_display = ("id", "order", "sub_product", "quantity", "final_price", "total_sum")
    list_display_links = ("id", "order", "sub_product")
    search_fields = ("order",)
