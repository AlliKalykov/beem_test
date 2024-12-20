# Generated by Django 5.1.2 on 2024-12-12 06:35

import abc_back.products.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_remove_subproduct_posters_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='poster',
        ),
        migrations.CreateModel(
            name='ProductPoster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
                ('is_published', models.BooleanField(default=False, verbose_name='опубликован')),
                ('image', models.ImageField(upload_to=abc_back.products.models.product_image_upload_to, verbose_name='Изображение')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Основное изображение')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posters', related_query_name='poster', to='products.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Постер',
                'verbose_name_plural': 'Постеры',
            },
        ),
    ]
