from __future__ import annotations

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from abc_back.mixins import TimestampedModelMixin


class AboutMe(TimestampedModelMixin):
    fio = models.CharField("ФИО", max_length=255)
    email = models.EmailField("Почта", max_length=255)
    phone = PhoneNumberField(verbose_name="Телефон")
    address = models.CharField("Страна, город", max_length=255)
    about_yourself = models.TextField("Расскажите о себе")

    objects = models.Manager()

    class Meta:
        verbose_name = "О клиенте"
        verbose_name_plural = "О клиентах"

    def __str__(self):
        return f"{self.fio} - {self.email}"


class Question(TimestampedModelMixin):
    name = models.CharField("Имя", max_length=255)
    email = models.EmailField("Почта", max_length=255)
    question = models.TextField("Сообщение")

    objects = models.Manager()

    class Meta:
        verbose_name = "Вопрос от клиента"
        verbose_name_plural = "Вопросы от клиентов"

    def __str__(self):
        return f"{self.name} - {self.email}"


class GiftCertificateOrder(TimestampedModelMixin):
    buyer_fio = models.CharField("ФИО покупателя", max_length=255)
    buyer_email = models.EmailField("Почта покупателя", max_length=255)
    addressee_name = models.CharField("Имя получателя", max_length=255)
    summa = models.DecimalField("Сумма сертификата", max_digits=10, decimal_places=2)
    addressee_message = models.TextField("Сообщение получателю")
    is_read = models.BooleanField("Прочтено", default=False)
    is_done = models.BooleanField("Выполнено", default=False)

    objects = models.Manager()

    class Meta:
        verbose_name = "Подарочный сертификат"
        verbose_name_plural = "Подарочные сертификаты"

    def __str__(self):
        return f"{self.buyer_fio} - {self.buyer_email}"
