from __future__ import annotations

from django.contrib import admin

from .models import AboutMe, GiftCertificateOrder, Question


@admin.register(AboutMe)
class AboutMeAdmin(admin.ModelAdmin):
    list_display = ("id", "fio", "email", "phone", "address", "created_at")
    list_display_links = ("id", "fio", "email")
    search_fields = ("id", "fio", "email", "phone", "address")
    list_filter = ("created_at",)


@admin.register(GiftCertificateOrder)
class GiftCertificateOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer_fio", "buyer_email", "summa", "is_read", "is_done", "created_at")
    list_display_links = ("id", "buyer_fio", "buyer_email")
    search_fields = ("id", "buyer_fio", "buyer_email", "summa")
    list_filter = ("created_at", "is_read", "is_done")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "created_at")
    list_display_links = ("id", "name", "email")
    search_fields = ("id", "name", "email", "question")
    list_filter = ("created_at",)
