from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    label_suffix = ''

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': _('Your name'), 'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': _('you@example.com'), 'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': _('+974 ...'), 'autocomplete': 'tel',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': _('What can we help with?'),
            }),
            'message': forms.Textarea(attrs={
                'placeholder': _('Tell us about your project...'), 'rows': 6,
            }),
        }
        labels = {
            'name': _('Name'),
            'email': _('Email'),
            'phone': _('Phone (optional)'),
            'subject': _('Subject'),
            'message': _('Message'),
        }
