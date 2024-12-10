# Generated by Django 5.1.2 on 2024-12-10 10:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField(default=0, verbose_name='Позиция')),
                ('name', models.CharField(max_length=36, unique=True, verbose_name='Страна')),
                ('slug', models.SlugField(max_length=36, unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveSmallIntegerField(default=0, verbose_name='Позиция')),
                ('name', models.CharField(max_length=36, unique=True, verbose_name='Город')),
                ('slug', models.SlugField(max_length=36, unique=True, verbose_name='Слаг')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', related_query_name='city', to='core.country', verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ['position'],
            },
        ),
    ]
