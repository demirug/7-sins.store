from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Feedback(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='Имя')
    timestamp = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=254, verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Тема сообщения')
    question = models.TextField(verbose_name='Сообщение', blank=False)
    answer = models.TextField(blank=True, verbose_name='Ответ')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__answer = self.answer

    def clean(self):
        if self.answer != self.__answer:
            self.sendEmail()

    def sendEmail(self):
        subject, from_email, to = 'Вопрос на сайте 7-sins.store', 'Answer Question', self.email

        html_content = render_to_string('feedback/email/feedback.html', {
            'name': self.full_name,
            'question': self.question,
            'answer': self.answer
        })

        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
