from adminsortable2.admin import SortableAdminMixin

from django.contrib import admin

from abc_back.mixins import ReadOnlyInlineMixin

from .models import City, Country


class CityInline(ReadOnlyInlineMixin, admin.TabularInline):
    model = City
    extra = 0


@admin.register(Country)
class CountryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")
    readonly_fields = ("position",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

    inlines = [CityInline]


@admin.register(City)
class CityAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("id", "name", "slug", "country")
    list_display_links = ("id", "country", "name")
    readonly_fields = ("position",)
    search_fields = ("name", "slug", "country__name")
    prepopulated_fields = {"slug": ("name",)}
