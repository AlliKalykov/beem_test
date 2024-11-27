from django.db import models


class SizeType(models.TextChoices):
    THINGS = "th", "Штук"
    MILLILITER = "ml", "Миллилитр"
    LITER = "l", "Литр"
    GRAM = "gr", "Грамм"
    KILOGRAM = "kg", "Килограмм"
