from django.contrib import admin

from abc_back.mixins import ReadOnlyAdminMixin
from abc_back.utils import render_object_changelist_link

from .models import Order, OrderItem


# TODO: добавить перед PROD ReadOnlyAdminMixin,
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

    @admin.display(description="Детали заказа")
    def order_items_link(self, obj):
        """Добавляет ссылку на OrderItemAdmin с фильтром по текущему заказу."""
        position_count = obj.order_items.count()
        return render_object_changelist_link(
            OrderItem.objects.first(), content=f"Детали заказа ({position_count})",
            query=f"order__id__exact={obj.pk}", new_tab=True,
        )


@admin.register(OrderItem)
class OrderItemAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("id", "order", "sub_product", "quantity", "final_price", "total_sum")
    list_display_links = ("id", "order", "sub_product")
    search_fields = ("order",)
