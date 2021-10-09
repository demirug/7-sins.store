from django.contrib import messages
from django.shortcuts import render, redirect

from feedback.forms import FeedbackModelForm


def feedback(request):
    form = FeedbackModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Вопрос был отправлен администрации')
        return redirect('home')
    else:
        return render(request, 'feedback/form.html', context={'form': form})