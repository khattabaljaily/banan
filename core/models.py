from django.db import models
from django.utils.translation import get_language
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
