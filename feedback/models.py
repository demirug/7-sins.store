from django.db import models

from .tasks import send_email_task


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
            send_email_task.delay(self.email, self.question, self.answer)
