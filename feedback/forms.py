from django import forms

from feedback.models import Feedback


class FeedbackModelForm(forms.ModelForm):
    full_name = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Тема сообщения', widget=forms.TextInput(attrs={'class': 'form-control'}))
    question = forms.CharField(label='Сообщение', required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Feedback
        fields = ['full_name', 'email', 'subject', 'question']
