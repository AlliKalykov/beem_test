# Generated by Django 5.1.2 on 2024-12-10 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subproduct',
            name='final_price',
            field=models.FloatField(default=0, verbose_name='Конечная цена'),
        ),
    ]
