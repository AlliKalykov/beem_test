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
