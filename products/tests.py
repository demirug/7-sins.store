from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from products.models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name='Test1', slug='test1', price=10.1, quantity=12)
        Product.objects.create(name='Test2', slug='test2', price=10.1, quantity=12)

    def test_slug_unique(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(name='Test3', slug='test1', price=10.1, quantity=12)

    def test_slug_generate_1(self):
        product = Product.objects.create(name='тест', price=10.1, quantity=12)
        product.clean()
        self.assertEqual(product.slug, 'pk__3')

    def test_slug_generate_2(self):
        product = Product.objects.create(name='test', price=10.1, quantity=12)
        product.clean()
        self.assertEqual(product.slug, 'test')

    def test_slug_generate_3(self):
        product = Product.objects.create(name='test', slug='pk__40', price=10.1, quantity=12)
        with self.assertRaises(ValidationError):
            product.clean()
