from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderItem(models.Model):
    product = models.ForeignKey('products.Product', null=True, on_delete=models.SET_NULL)
    count = models.PositiveIntegerField()
    price = models.FloatField(default=-1)

    def calcPrice(self):
        return self.price * self.count

    def clean(self):
        if self.pk is None:
            self.price = self.product.price

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name + ' | ' + str(self.count) + ' item'


class Order(models.Model):

    orderItems = models.ManyToManyField(OrderItem)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=300, blank=True)
    additional = models.TextField(blank=True, null=True)

    class StatusChoice(models.TextChoices):
        NEW = 'NEW', _('Новый')
        ACCEPTED = 'ACCEPTED', _('Принят')
        CANCELED = 'CANCELED', _('Отменен')
        DONE = 'DONE', _('Выполнен')

    status = models.CharField(max_length=8, choices=StatusChoice.choices, default=StatusChoice.NEW)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__status = self.status

    def __updateStatus(self):
        from orders.tasks import send_email_task

        if self.__status == self.StatusChoice.DONE or self.__status == self.StatusChoice.CANCELED or self.status == self.StatusChoice.NEW:
            raise ValidationError(f'Изменение на данный статус запрещено')

        elif self.status == self.StatusChoice.ACCEPTED:
            for ordItem in self.orderItems.all():
                if ordItem.product:
                    if ordItem.product.quantity == 0 or ordItem.product.quantity - ordItem.count < 0:
                        raise ValidationError(f'Необходимого количество продукции {str(ordItem.product)} нет в наличии!')
                    ordItem.product.quantity -= ordItem.count
                    ordItem.product.save()
        elif self.status == self.StatusChoice.CANCELED:
            if self.__status == self.StatusChoice.ACCEPTED:
                for ordItem in self.orderItems.all():
                    if ordItem.product:
                        ordItem.product.quantity += ordItem.count
                        ordItem.product.save()
        send_email_task.delay(self.status, self.pk)

    def clean(self):
        if self.status != self.__status:
            self.__updateStatus()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__status = self.status

    def __str__(self):
        return 'Заказ №' + str(self.pk) + ' | ' + self.status
