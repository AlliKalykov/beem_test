# Generated by Django 5.1.2 on 2024-11-28 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='color',
            old_name='color',
            new_name='name',
        ),
        migrations.AddField(
            model_name='color',
            name='hex_code',
            field=models.CharField(default=1, max_length=24, unique=True, verbose_name='Шестнадцатеричный код'),
            preserve_default=False,
        ),
    ]
