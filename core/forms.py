from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage, WebsiteRequest


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


class WebsiteRequestForm(forms.ModelForm):
    label_suffix = ''

    # Declared explicitly (rather than left to the ModelForm) so Django doesn't
    # insert its usual blank "---------" choice for a required field with no
    # model default — with RadioSelect that blank choice renders as its own
    # selectable (and pre-checked) button, which we don't want.
    website_type = forms.ChoiceField(
        choices=WebsiteRequest.WEBSITE_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label=_('What type of website do you need?'),
    )
    timeline = forms.ChoiceField(
        choices=WebsiteRequest.TIMELINE_CHOICES,
        widget=forms.RadioSelect,
        label=_('When do you need it?'),
    )
    features = forms.MultipleChoiceField(
        choices=WebsiteRequest.FEATURE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label=_('Which features do you need?'),
    )

    class Meta:
        model = WebsiteRequest
        fields = [
            'name', 'email', 'phone', 'company',
            'website_type', 'budget_range', 'timeline',
            'features', 'reference_sites', 'details',
        ]
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
            'company': forms.TextInput(attrs={
                'placeholder': _('Company name'), 'autocomplete': 'organization',
            }),
            'budget_range': forms.RadioSelect,
            'reference_sites': forms.TextInput(attrs={
                'placeholder': _('e.g. example.com, another-example.com'),
            }),
            'details': forms.Textarea(attrs={
                'placeholder': _('Tell us more about your project, goals and any specific requirements...'),
                'rows': 6,
            }),
        }
        labels = {
            'name': _('Name'),
            'email': _('Email'),
            'phone': _('Phone'),
            'company': _('Company (optional)'),
            'budget_range': _('Estimated budget'),
            'reference_sites': _('Websites you like (optional)'),
            'details': _('Project details'),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.features = ','.join(self.cleaned_data.get('features', []))
        if commit:
            instance.save()
        return instance
