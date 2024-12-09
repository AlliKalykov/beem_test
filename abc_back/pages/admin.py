from __future__ import annotations

from django.contrib import admin

from abc_back.pages.models import AboutUs, Contact, Delivery, GiftCertificate


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "sub_title", "is_featured")
    list_display_links = ("id", "title", "sub_title")
    search_fields = ("title", "sub_title")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone", "is_featured")
    list_display_links = ("id", "email")
    search_fields = ("email",)


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_featured")
    list_display_links = ("id", "title")
    search_fields = ("title", "text")


@admin.register(GiftCertificate)
class GiftCertificateAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_featured")
    list_display_links = ("id", "title")
    search_fields = ("title", "subtext")
