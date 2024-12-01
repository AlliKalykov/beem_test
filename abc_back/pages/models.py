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

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"

    def __str__(self):
        return self.title


class Delivery(models.Model):
    title = models.TextField("Заголовок")
    main_poster = models.FileField("Постер")
    text = models.TextField("Текст")
    email = models.EmailField("Электронная почта", max_length=255)
    phone = models.CharField("Номер телефона", max_length=20)
    whatsapp = models.CharField("WhatsApp номер", max_length=255)
    telegram = models.CharField("Telegram номер", max_length=255)

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставка"

    def __str__(self):
        return self.title