from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название товара')
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True, unique=True)
    price = models.FloatField(default=0, verbose_name='Цена')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара')
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['quantity', 'name']
