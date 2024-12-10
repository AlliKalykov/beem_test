from django.db import models


class CreatedAtModelMixin(models.Model):
    """Миксин для отслеживания даты создания объекта."""

    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)

    class Meta:
        abstract = True


class UpdatedAtModelMixin(models.Model):
    """Миксин для отслеживания последней даты обновления."""

    updated_at = models.DateTimeField(verbose_name="дата обновления", auto_now=True)

    class Meta:
        abstract = True


class TimestampedModelMixin(CreatedAtModelMixin, UpdatedAtModelMixin):
    """Миксин для отслеживания дат создания и обновления объекта."""

    class Meta:
        abstract = True


class PublishedModelMixin(models.Model):
    """Миксин для отслеживания публикации объекта."""

    is_published = models.BooleanField(verbose_name="опубликован", default=False)

    class Meta:
        abstract = True


class SortableModelMixin(models.Model):
    position = models.PositiveSmallIntegerField("Позиция", default=0, blank=False, null=False)

    class Meta:
        abstract = True


class ReadOnlyInlineMixin:

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
