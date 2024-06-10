from django import forms

from mailings.models import Mail, Mailing
from users.forms import StyleFormMixin


class MailForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mail
        fields = ('subject', 'body')


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('send_time', 'first_send_date', 'frequency')
        widgets = {
            'first_send_date': forms.DateInput(attrs={'type': 'date'}),
            'send_time': forms.TimeInput(attrs={'type': 'time'}),
        }
