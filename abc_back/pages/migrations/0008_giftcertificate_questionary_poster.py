# Generated by Django 5.1.2 on 2024-12-12 06:44

import abc_back.pages.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftcertificate',
            name='questionary_poster',
            field=models.FileField(blank=True, null=True, upload_to=abc_back.pages.models.file_upload_to, verbose_name='Постер анкеты'),
        ),
    ]