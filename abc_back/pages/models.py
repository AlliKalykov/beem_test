from django.db import models

from abc_back.utils import generate_filename


def file_upload_to(instance, filename):
    new_filename = generate_filename(filename)
    return f"pages/{new_filename}"


class AboutUs(models.Model):
    title = models.TextField("Заголовок")
    sub_title = models.TextField("Подзаголовок")
    main_poster = models.FileField("Постер", upload_to=file_upload_to, blank=True, null=True)
    about_title = models.TextField("Заголовок о нас")
    about_text = models.TextField("Текст о нас")
    about_poster = models.FileField("Постер о нас", upload_to=file_upload_to, blank=True, null=True)
    work_title = models.TextField("Заголовок работы")
    work_text = models.TextField("Текст работы")
    work_poster = models.FileField("Постер работы", upload_to=file_upload_to, blank=True, null=True)
    is_featured = models.BooleanField("Основное", default=False)

    objects = models.Manager()

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_featured:
            AboutUs.objects.exclude(pk=self.pk).update(is_featured=False)
        super().save(*args, **kwargs)


class Delivery(models.Model):
    title = models.TextField("Заголовок")
    main_poster = models.FileField("Постер", upload_to=file_upload_to, blank=True, null=True)
    text = models.TextField("Текст")
    email = models.EmailField("Электронная почта", max_length=255)
    phone = models.CharField("Номер телефона", max_length=20)
    whatsapp = models.CharField("WhatsApp номер", max_length=255)
    telegram = models.CharField("Telegram номер", max_length=255)
    is_featured = models.BooleanField("Основное", default=False)

    objects = models.Manager()

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставка"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_featured:
            Delivery.objects.exclude(pk=self.pk).update(is_featured=False)
        super().save(*args, **kwargs)


class GiftCertificate(models.Model):
    main_poster = models.FileField("Постер", upload_to=file_upload_to, blank=True, null=True)
    title = models.TextField("Заголовок")
    subtext = models.TextField("Подтекст")
    email = models.EmailField("Электронная почта", max_length=255)
    phone = models.CharField("Номер телефона", max_length=20)
    whatsapp = models.CharField("WhatsApp номер", max_length=255)
    telegram = models.CharField("Telegram номер", max_length=255)
    is_featured = models.BooleanField("Основное", default=False)

    objects = models.Manager()

    class Meta:
        verbose_name = "Подарочный сертификат"
        verbose_name_plural = "Подарочный сертификат"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_featured:
            GiftCertificate.objects.exclude(pk=self.pk).update(is_featured=False)
        super().save(*args, **kwargs)
