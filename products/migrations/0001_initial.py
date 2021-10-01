# Generated by Django 3.2.7 on 2021-10-01 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название товара')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена')),
                ('description', models.TextField(blank=True, verbose_name='Описание товара')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество товара')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['quantity', 'name'],
            },
        ),
    ]
