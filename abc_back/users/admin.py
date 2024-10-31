from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.functions import Collate
from django_celery_beat.admin import ClockedScheduleAdmin as _ClockedScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as _PeriodicTaskAdmin
from django_celery_beat.models import ClockedSchedule, CrontabSchedule, IntervalSchedule, PeriodicTask, SolarSchedule

from abc_back.admin import SuperUserModuleMixin
from abc_back.users.models import User
from abc_back.utils import set_attrs


admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ["id", "email", "full_name", "is_active"]
    list_display_links = ["id", "email", "full_name"]
    search_fields = ["id", "email_deterministic", "first_name", "last_name"]
    list_filter = ["is_active", "is_staff", "is_superuser"]
    ordering = ["email"]
    fieldsets = [
        ("Персональная информация", {
            "fields": ["email", "password", "phone", "first_name", "last_name", "middle_name", "profile_image"],
        }),
        ("Дополнительные данные", {
            "fields": ["gender", "date_of_birth"],
        }),
        ("Настройки", {
            "fields": ["is_active"],
        }),
        ("Техническая информация", {
            "fields": [
                "is_staff", "is_superuser", "last_login", "date_joined", "groups",
            ],
        }),
    ]
    add_fieldsets = (
        (
            "Общая информация",
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    read_only_fields = ["last_login", "date_joined"]

    filter_horizontal = ["groups"]

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .prefetch_related("groups")
            .annotate(email_deterministic=Collate("email", "und-x-icu"))
        )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    @set_attrs(short_description="Группы")
    def group_list(self, obj: User) -> str:
        return ", ".join(obj.groups.values_list("name", flat=True))

    @set_attrs(short_description="ФИО")
    def full_name(self, obj: User) -> str:
        return obj.full_name


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(SuperUserModuleMixin, admin.ModelAdmin):
    ...


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(SuperUserModuleMixin, admin.ModelAdmin):
    ...


@admin.register(SolarSchedule)
class SolarScheduleAdmin(SuperUserModuleMixin, admin.ModelAdmin):
    ...


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(SuperUserModuleMixin, _ClockedScheduleAdmin):
    ...


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(SuperUserModuleMixin, _PeriodicTaskAdmin):
    ...
