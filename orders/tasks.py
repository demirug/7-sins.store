from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from seven_sins_store.celery import app
from .models import Order


@app.task()
def send_email_task(status, pk):

    object: Order = Order.objects.filter(pk=pk).first()
    if not object:
        return

    subject, from_email, to = 'Заказ на сайте 7-sins.store', 'Track Info', object.email

    html_content = render_to_string('orders/email/status/' + status + '.html', {
        'pk': pk,
        'products': object.orderItems.all(),
        'totalPrice': object.price
    })

    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
