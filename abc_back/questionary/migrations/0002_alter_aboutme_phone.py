# Generated by Django 5.1.2 on 2024-12-08 17:01

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutme',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default="+996777777777", max_length=128, region=None, verbose_name='Телефон'),
            preserve_default=False,
        ),
    ]
