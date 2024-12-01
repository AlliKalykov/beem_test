from __future__ import annotations

from django.contrib import admin

from abc_back.pages.models import AboutUs, Delivery


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("title", "sub_title")
    list_display_links = ("title", "sub_title")
    search_fields = ("title", "sub_title")

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("title", "text")
    list_display_links = ("title", "text")
    search_fields = ("title", "text")
