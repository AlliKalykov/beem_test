# Generated by Django 5.1.2 on 2024-12-09 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_aboutus_is_featured_delivery_is_featured_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Электронная почта')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='Город')),
                ('street', models.CharField(blank=True, max_length=255, null=True, verbose_name='Улица')),
                ('house', models.CharField(blank=True, max_length=255, null=True, verbose_name='Дом')),
                ('schedule', models.TextField(blank=True, null=True, verbose_name='График работы')),
                ('instagram', models.URLField(blank=True, max_length=48, null=True, verbose_name='Instagram')),
                ('whatsapp', models.URLField(blank=True, max_length=48, null=True, verbose_name='WhatsApp номер')),
                ('telegram', models.URLField(blank=True, max_length=48, null=True, verbose_name='Telegram ')),
                ('facebook', models.URLField(blank=True, max_length=48, null=True, verbose_name='Facebook')),
                ('xcom', models.URLField(blank=True, max_length=48, null=True, verbose_name='Твиттер')),
                ('vk', models.URLField(blank=True, max_length=48, null=True, verbose_name='Вконтакте')),
                ('tiktok', models.URLField(blank=True, max_length=48, null=True, verbose_name='Тикток')),
                ('youtube', models.URLField(blank=True, max_length=48, null=True, verbose_name='Ютуб')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Основное')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
            },
        ),
    ]
