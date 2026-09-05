from django.db import models
from django.utils.translation import get_language, gettext_lazy as _
from django.utils.text import slugify


class BilingualMixin:
    """Resolves an *_en / *_ar field pair based on the active language."""

    def _localized(self, field):
        lang = get_language()
        value = getattr(self, f'{field}_ar', None) if lang and lang.startswith('ar') else None
        return value or getattr(self, f'{field}_en')


class Service(BilingualMixin, models.Model):
    ICON_CHOICES = [
        ('code', 'Code / Development'),
        ('cloud', 'Cloud / IT Services'),
        ('cart', 'E-commerce / Retail'),
        ('shield', 'Security / Consulting'),
        ('chart', 'Data / Analytics'),
        ('devices', 'Devices / Integration'),
        ('globe', 'Website / Web'),
        ('support', 'Technical Support'),
    ]

    name_en = models.CharField(max_length=120)
    name_ar = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default='code')
    summary_en = models.CharField(max_length=240)
    summary_ar = models.CharField(max_length=240)
    description_en = models.TextField()
    description_ar = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name_en

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

    @property
    def name(self):
        return self._localized('name')

    @property
    def summary(self):
        return self._localized('summary')

    @property
    def description(self):
        return self._localized('description')


class Project(BilingualMixin, models.Model):
    title_en = models.CharField(max_length=160)
    title_ar = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    summary_en = models.CharField(max_length=240)
    summary_ar = models.CharField(max_length=240)
    description_en = models.TextField(blank=True)
    description_ar = models.TextField(blank=True)
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    external_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title_en

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)

    @property
    def title(self):
        return self._localized('title')

    @property
    def summary(self):
        return self._localized('summary')

    @property
    def description(self):
        return self._localized('description')


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=160, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} <{self.email}> - {self.created_at:%Y-%m-%d}'


class WebsiteRequest(models.Model):
    """A visitor's project brief for a new website — the dedicated intake
    form for the Website Development service. Modeled on a full client
    discovery questionnaire (company, goals, content, integrations, legal,
    hosting, post-launch needs, timeline, then budget last), so most fields
    are optional — visitors answer what's relevant to their project."""

    YES_NO_CHOICES = [
        ('yes', _('Yes')),
        ('no', _('No')),
    ]

    WEBSITE_TYPE_CHOICES = [
        ('business', _('Business / corporate website')),
        ('ecommerce', _('Online store (e-commerce)')),
        ('portfolio', _('Portfolio / personal website')),
        ('landing', _('Landing page for a campaign or product')),
        ('webapp', _('Web application / custom system')),
        ('other', _('Something else')),
    ]

    WEBSITE_GOAL_CHOICES = [
        ('introduce', _('Introduce the company and its services')),
        ('attract', _('Attract new customers')),
        ('inquiries', _('Receive customer inquiries')),
        ('sell_online', _('Sell products or services online')),
        ('requests_online', _('Let customers submit requests online')),
        ('branches', _('Showcase branches and locations')),
    ]

    LANGUAGE_CHOICES = [
        ('ar', _('Arabic only')),
        ('en', _('English only')),
        ('both', _('Arabic + English')),
    ]

    CONTACT_CHANNEL_CHOICES = [
        ('whatsapp', _('WhatsApp')),
        ('form', _('Contact form')),
        ('call', _('Direct phone call')),
        ('email', _('Email')),
        ('social', _('Social media links')),
    ]

    FEATURE_CHOICES = [
        ('accounts', _('Customer account creation & login')),
        ('documents', _('Document upload')),
        ('requests', _('Submit requests or orders online')),
        ('tracking', _('Track request/order status')),
        ('payments', _('Online payment')),
        ('booking', _('Booking or appointments')),
        ('blog', _('Blog or news section')),
        ('cms', _('Admin panel to edit content myself')),
        ('seo', _('SEO optimization')),
        ('app', _('Mobile app integration')),
    ]

    LEGAL_REQUIREMENT_CHOICES = [
        ('privacy', _('Privacy policy')),
        ('terms', _('Terms and conditions')),
        ('disclaimer', _('Disclaimer')),
        ('license', _('License / regulatory information')),
    ]

    CONTENT_READINESS_CHOICES = [
        ('ready', _('Content is fully ready on our side')),
        ('need_help', _('We need full help preparing the content')),
        ('mixed', _('A mix of both')),
    ]

    POST_LAUNCH_CHOICES = [
        ('content', _('Edit page content')),
        ('products', _('Add or update products/services')),
        ('branches', _('Add or remove branches')),
        ('requests', _('Manage customer requests')),
        ('news', _('Manage news and promotions')),
    ]

    BUDGET_CHOICES = [
        ('under_5k', _('Under 5,000 QAR')),
        ('5k_15k', _('5,000 – 15,000 QAR')),
        ('15k_30k', _('15,000 – 30,000 QAR')),
        ('30k_plus', _('30,000+ QAR')),
    ]

    ANALYTICS_CHOICES = [
        ('ga', _('Google Analytics')),
        ('fb', _('Facebook Pixel')),
        ('gtm', _('Google Tag Manager')),
        ('unsure', _("Not sure — recommend what's best")),
    ]

    TIMELINE_CHOICES = [
        ('asap', _('As soon as possible')),
        ('1_month', _('Within a month')),
        ('1_3_months', _('1–3 months')),
        ('flexible', _('Flexible / just exploring')),
    ]

    # 1. Your details
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    company = models.CharField(max_length=160, blank=True)

    # 2. About your company
    company_description = models.TextField(blank=True)
    branches_count = models.CharField(max_length=20, blank=True)
    has_brand_identity = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True)

    # 3. About your website
    website_type = models.CharField(max_length=20, choices=WEBSITE_TYPE_CHOICES)
    website_goals = models.CharField(max_length=255, blank=True)
    other_goal = models.CharField(max_length=200, blank=True)

    # 4. Products & services
    services_offered = models.TextField(blank=True)

    # 5. Branches & locations
    has_branches = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True)
    branches_details = models.TextField(blank=True)

    # 6. Language
    language_preference = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)

    # 7. Customer communication
    contact_channels = models.CharField(max_length=255, blank=True)
    contact_channels_details = models.TextField(blank=True)

    # 8. Online / electronic services
    features = models.CharField(max_length=255, blank=True)
    online_services_details = models.TextField(blank=True)

    # 9. System integration
    has_existing_system = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True)
    needs_integration = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True)
    integration_details = models.TextField(blank=True)

    # 10. Legal & compliance
    legal_requirements = models.CharField(max_length=255, blank=True)
    other_legal = models.CharField(max_length=200, blank=True)

    # 11. Content readiness
    content_readiness = models.CharField(max_length=20, choices=CONTENT_READINESS_CHOICES)

    # 12. Hosting & domain
    has_domain_hosting = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True)
    needs_domain_hosting_help = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True)

    # 13. Design references
    reference_sites = models.CharField(max_length=500, blank=True)

    # 14. Post-launch management
    post_launch_control = models.CharField(max_length=255, blank=True)

    # 15. Timeline
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES)
    has_specific_date = models.CharField(max_length=3, choices=YES_NO_CHOICES, blank=True)
    target_date = models.DateField(null=True, blank=True)

    # 16. Planning & budget
    target_audience = models.TextField(blank=True)
    analytics_tools = models.CharField(max_length=255, blank=True)
    success_criteria = models.TextField(blank=True)
    preferred_domain = models.CharField(max_length=200, blank=True)
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES)

    # 17. Anything else
    details = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} <{self.email}> - {self.created_at:%Y-%m-%d}'

    def _choice_list_display(self, field_name, choices):
        labels = dict(choices)
        raw = getattr(self, field_name) or ''
        return [labels.get(key, key) for key in raw.split(',') if key]

    def website_goals_display(self):
        return self._choice_list_display('website_goals', self.WEBSITE_GOAL_CHOICES)

    def contact_channels_display(self):
        return self._choice_list_display('contact_channels', self.CONTACT_CHANNEL_CHOICES)

    def features_display(self):
        return self._choice_list_display('features', self.FEATURE_CHOICES)

    def legal_requirements_display(self):
        return self._choice_list_display('legal_requirements', self.LEGAL_REQUIREMENT_CHOICES)

    def post_launch_control_display(self):
        return self._choice_list_display('post_launch_control', self.POST_LAUNCH_CHOICES)

    def analytics_tools_display(self):
        return self._choice_list_display('analytics_tools', self.ANALYTICS_CHOICES)
