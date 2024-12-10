from __future__ import annotations

from django.db import models


class OrderStatus(models.TextChoices):
    DRAFT = "draft" "Черновик"
    NEW = "new" "Новый"
    CONFIRMED = "confirmed" "Подтвержден"
    PAYED = "payed" "Оплачен"
    IN_DELIVERY = "in_delivery" "В доставке"
    DELIVERED = "delivered" "Доставлен"
    CANCELED = "canceled" "Отменен"
    RETURNED = "returned" "Возврат"
