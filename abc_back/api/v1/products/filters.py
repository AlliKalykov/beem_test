from __future__ import annotations

from django.db.models import Exists, OuterRef

from django_filters import rest_framework as drf_filters

from abc_back.products.models import Product, SubProduct


class NumberInFilter(drf_filters.BaseInFilter, drf_filters.NumberFilter):
    pass


class ProductFilterSet(drf_filters.FilterSet):
    category = NumberInFilter(field_name="category__id", lookup_expr="in")
    brand = NumberInFilter(field_name="brand__id", lookup_expr="in")
    is_novelty = drf_filters.BooleanFilter(field_name="is_novelty", lookup_expr="exact")
    is_bestseller = drf_filters.BooleanFilter(field_name="is_bestseller", lookup_expr="exact")
    is_back_in_stock = drf_filters.BooleanFilter(field_name="is_back_in_stock", lookup_expr="exact")
    is_recommendation = drf_filters.BooleanFilter(field_name="is_recommendation", lookup_expr="exact")

    price_min = drf_filters.NumberFilter(method="filter_price_min")
    price_max = drf_filters.NumberFilter(method="filter_price_max")

    class Meta:
        model = Product
        fields = []

    def filter_price_min(self, queryset, name, value):
        if value:
            return queryset.filter(
                Exists(
                    SubProduct.objects.filter(
                        product_id=OuterRef("id"),
                        final_price__gte=value,
                        is_available=True,
                    )
                )
            )
        return queryset

    def filter_price_max(self, queryset, name, value):
        if value:
            return queryset.filter(
                Exists(
                    SubProduct.objects.filter(
                        product_id=OuterRef("id"),
                        final_price__lte=value,
                        is_available=True,
                    )
                )
            )
        return queryset
