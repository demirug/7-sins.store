from datetime import timedelta, datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from orders.models import Order
from seven_sins_store import settings
from seven_sins_store.celery import app


@app.task()
def send_admin_email_task():

    yesterday = datetime.now() - timedelta(days=1)
    orders = Order.objects.filter(timestamp__gte=yesterday, status=Order.StatusChoice.NEW)

    if len(orders) == 0:
        return

    subject, from_email, to = 'Произведенные заказы за ' + str(yesterday.date()), 'Orders', settings.ADMIN_EMAILS.split(';')

    html_content = render_to_string('manager/email/admin_info.html', context={
        'objects': orders
    })

    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
