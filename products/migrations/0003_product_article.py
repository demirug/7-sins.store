# Generated by Django 3.2.7 on 2021-10-08 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='article',
            field=models.CharField(blank=True, max_length=100, verbose_name='Артикул'),
        ),
    ]
