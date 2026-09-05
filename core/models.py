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
    form for the Website Development service, richer than the general
    contact form."""

    WEBSITE_TYPE_CHOICES = [
        ('business', _('Business / corporate website')),
        ('ecommerce', _('Online store (e-commerce)')),
        ('portfolio', _('Portfolio / personal website')),
        ('landing', _('Landing page for a campaign or product')),
        ('webapp', _('Web application / custom system')),
        ('other', _('Something else')),
    ]

    BUDGET_CHOICES = [
        ('under_5k', _('Under 5,000 QAR')),
        ('5k_15k', _('5,000 – 15,000 QAR')),
        ('15k_30k', _('15,000 – 30,000 QAR')),
        ('30k_plus', _('30,000+ QAR')),
    ]

    TIMELINE_CHOICES = [
        ('asap', _('As soon as possible')),
        ('1_month', _('Within a month')),
        ('1_3_months', _('1–3 months')),
        ('flexible', _('Flexible / just exploring')),
    ]

    FEATURE_CHOICES = [
        ('multilingual', _('Multi-language (Arabic & English)')),
        ('ecommerce', _('Online payments / store')),
        ('booking', _('Booking or appointments')),
        ('blog', _('Blog or news section')),
        ('cms', _('Admin panel to edit content myself')),
        ('seo', _('SEO optimization')),
        ('app', _('Mobile app integration')),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    company = models.CharField(max_length=160, blank=True)
    website_type = models.CharField(max_length=20, choices=WEBSITE_TYPE_CHOICES)
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES)
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES)
    features = models.CharField(max_length=255, blank=True)
    reference_sites = models.CharField(max_length=500, blank=True)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} <{self.email}> - {self.created_at:%Y-%m-%d}'

    def features_display(self):
        labels = dict(self.FEATURE_CHOICES)
        return [labels.get(key, key) for key in self.features.split(',') if key]
