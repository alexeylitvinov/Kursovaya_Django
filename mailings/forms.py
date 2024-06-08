from django import forms

from mailings.models import Mail
from users.forms import StyleFormMixin


class MailForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mail
        fields = ('subject', 'body')
