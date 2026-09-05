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
    """A full project-brief intake form, modeled on a client discovery
    questionnaire: company, website goals, content, integrations, legal,
    hosting, post-launch needs and timeline — budget comes last. Most
    questions are optional since not every section applies to every
    business; only the essentials are required.

    Every choice/multi-choice field below is declared explicitly (rather
    than left to the ModelForm) so Django doesn't insert its usual blank
    "---------" choice — with RadioSelect/CheckboxSelectMultiple that blank
    choice would render as its own selectable (and sometimes pre-checked)
    button, which we don't want.
    """

    MULTI_CHOICE_FIELDS = (
        'website_goals', 'contact_channels', 'features',
        'legal_requirements', 'post_launch_control', 'analytics_tools',
    )

    # --- About your website ---
    website_type = forms.ChoiceField(
        choices=WebsiteRequest.WEBSITE_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label=_('What type of website do you need?'),
    )
    website_goals = forms.MultipleChoiceField(
        choices=WebsiteRequest.WEBSITE_GOAL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label=_('What is the main goal of the website? (select all that apply)'),
    )

    # --- Branches & locations ---
    has_branches = forms.ChoiceField(
        choices=WebsiteRequest.YES_NO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label=_('Do you have multiple branches or locations?'),
    )

    # --- About your company ---
    has_brand_identity = forms.ChoiceField(
        choices=WebsiteRequest.YES_NO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label=_('Do you already have a logo and brand identity?'),
    )

    # --- Language ---
    language_preference = forms.ChoiceField(
        choices=WebsiteRequest.LANGUAGE_CHOICES,
        widget=forms.RadioSelect,
        label=_('Which languages should the website support?'),
    )

    # --- Customer communication ---
    contact_channels = forms.MultipleChoiceField(
        choices=WebsiteRequest.CONTACT_CHANNEL_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label=_('How should customers reach you through the site?'),
    )

    # --- Online / electronic services ---
    features = forms.MultipleChoiceField(
        choices=WebsiteRequest.FEATURE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label=_('Which features do you need?'),
    )

    # --- System integration ---
    has_existing_system = forms.ChoiceField(
        choices=WebsiteRequest.YES_NO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label=_('Do you have an existing internal system (ERP / POS / CRM)?'),
    )
    needs_integration = forms.ChoiceField(
        choices=WebsiteRequest.YES_NO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label=_('Should the website connect to that system, or any other API?'),
    )

    # --- Legal & compliance ---
    legal_requirements = forms.MultipleChoiceField(
        choices=WebsiteRequest.LEGAL_REQUIREMENT_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label=_('Do you need any of the following on the site?'),
    )

    # --- Content readiness ---
    content_readiness = forms.ChoiceField(
        choices=WebsiteRequest.CONTENT_READINESS_CHOICES,
        widget=forms.RadioSelect,
        label=_('Is your content — text, photos — ready, or do you need help preparing it?'),
    )

    # --- Hosting & domain ---
    has_domain_hosting = forms.ChoiceField(
        choices=WebsiteRequest.YES_NO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label=_('Do you already have a domain name and hosting?'),
    )
    needs_domain_hosting_help = forms.ChoiceField(
        choices=WebsiteRequest.YES_NO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label=_('Would you like us to handle the domain & hosting for you?'),
    )

    # --- Post-launch management ---
    post_launch_control = forms.MultipleChoiceField(
        choices=WebsiteRequest.POST_LAUNCH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label=_('After launch, what would you like to manage yourselves?'),
    )

    # --- Timeline ---
    timeline = forms.ChoiceField(
        choices=WebsiteRequest.TIMELINE_CHOICES,
        widget=forms.RadioSelect,
        label=_('When do you need it?'),
    )
    has_specific_date = forms.ChoiceField(
        choices=WebsiteRequest.YES_NO_CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label=_('Do you have a specific launch date in mind?'),
    )
    target_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label=_('Target date (optional)'),
    )

    # --- Planning & budget ---
    analytics_tools = forms.MultipleChoiceField(
        choices=WebsiteRequest.ANALYTICS_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label=_('Which analytics or tracking tools do you need? (optional)'),
    )
    budget_range = forms.ChoiceField(
        choices=WebsiteRequest.BUDGET_CHOICES,
        widget=forms.RadioSelect,
        label=_('Estimated budget'),
    )

    class Meta:
        model = WebsiteRequest
        fields = [
            'name', 'email', 'phone', 'company',
            'company_description', 'branches_count', 'has_brand_identity',
            'website_type', 'website_goals', 'other_goal',
            'services_offered',
            'has_branches', 'branches_details',
            'language_preference',
            'contact_channels', 'contact_channels_details',
            'features', 'online_services_details',
            'has_existing_system', 'needs_integration', 'integration_details',
            'legal_requirements', 'other_legal',
            'content_readiness',
            'has_domain_hosting', 'needs_domain_hosting_help',
            'reference_sites',
            'post_launch_control',
            'timeline', 'has_specific_date', 'target_date',
            'target_audience', 'analytics_tools', 'success_criteria', 'preferred_domain', 'budget_range',
            'details',
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
            'company_description': forms.Textarea(attrs={
                'placeholder': _('Briefly describe your company and what you do...'), 'rows': 3,
            }),
            'branches_count': forms.TextInput(attrs={'placeholder': _('e.g. 3')}),
            'other_goal': forms.TextInput(attrs={'placeholder': _('Describe another goal, if any')}),
            'services_offered': forms.Textarea(attrs={
                'placeholder': _("List the products or services you'd like to showcase..."), 'rows': 4,
            }),
            'branches_details': forms.Textarea(attrs={
                'placeholder': _("List each branch's address, phone number and working hours..."), 'rows': 3,
            }),
            'contact_channels_details': forms.Textarea(attrs={
                'placeholder': _('Numbers, links or email addresses for the channels above...'), 'rows': 2,
            }),
            'online_services_details': forms.Textarea(attrs={
                'placeholder': _('Describe what customers should be able to do, in detail...'), 'rows': 3,
            }),
            'integration_details': forms.Textarea(attrs={
                'placeholder': _('System name, and the type of integration needed...'), 'rows': 2,
            }),
            'other_legal': forms.TextInput(attrs={'placeholder': _('Other legal text or requirements')}),
            'reference_sites': forms.TextInput(attrs={
                'placeholder': _('e.g. example.com, another-example.com'), 'dir': 'ltr',
            }),
            'target_audience': forms.Textarea(attrs={
                'placeholder': _('e.g. individuals, businesses, a specific community...'), 'rows': 2,
            }),
            'success_criteria': forms.Textarea(attrs={
                'placeholder': _('e.g. number of visits, orders placed, calls received...'), 'rows': 2,
            }),
            'preferred_domain': forms.TextInput(attrs={'placeholder': 'example.com', 'dir': 'ltr'}),
            'details': forms.Textarea(attrs={
                'placeholder': _('Anything else we should know about your project...'), 'rows': 5,
            }),
        }
        labels = {
            'company': _('Company (optional)'),
            'company_description': _('Briefly describe your company'),
            'branches_count': _('How many branches or locations do you have? (optional)'),
            'other_goal': _('Another goal (optional)'),
            'services_offered': _('What products or services should the website showcase? (optional)'),
            'branches_details': _('Branch details (optional)'),
            'contact_channels_details': _('Channel details (optional)'),
            'online_services_details': _('Describe the online services you need (optional)'),
            'integration_details': _('Integration details (optional)'),
            'other_legal': _('Other legal requirements (optional)'),
            'reference_sites': _('Websites you like (optional)'),
            'target_audience': _('Who is your target audience? (optional)'),
            'success_criteria': _("How will you measure the website's success? (optional)"),
            'preferred_domain': _('Preferred domain name (optional)'),
            'details': _('Anything else we should know? (optional)'),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        for field in self.MULTI_CHOICE_FIELDS:
            setattr(instance, field, ','.join(self.cleaned_data.get(field, [])))
        if commit:
            instance.save()
        return instance
