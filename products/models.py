from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название товара')
    article = models.CharField(max_length=100, verbose_name='Артикул', blank=True)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True)
    price = models.FloatField(default=0, verbose_name='Цена')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество товара')
    image = models.ImageField(upload_to='product', null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view', args=[self.slug, self.pk])

    def validateSlug(self):
        # If slug not generated
        if not self.slug:
            self.slug = slugify(self.name)
        # If slug has pk construction
        if not self.slug:
            # If pk not setted save model
            if not self.pk:
                super().save()
            # Generate new slug if slug dont exists and it cant be generated by slugify
            self.slug = str(self.pk)

    def validateQuantity(self):
        if self.quantity < 0:
            raise ValidationError('Количество товара должно быть >= 0')

    def clean(self):
        self.validateSlug()
        self.validateQuantity()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['quantity', 'name']
