from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from seven_sins_store.celery import app


@app.task()
def send_email_task(email, question, answer):

    subject, from_email, to = 'Вопрос на сайте 7-sins.store', 'Answer Question', email

    html_content = render_to_string('feedback/email/feedback.html', {
        'question': question,
        'answer': answer
    })

    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
