from django.conf import settings


def site_meta(request):
    from .models import Service

    return {
        'COMPANY_NAME': settings.COMPANY_NAME,
        'COMPANY_NAME_AR': settings.COMPANY_NAME_AR,
        'COMPANY_CR_NUMBER': settings.COMPANY_CR_NUMBER,
        'COMPANY_PHONE': settings.COMPANY_PHONE,
        'COMPANY_PHONE_TEL': settings.COMPANY_PHONE_TEL,
        'COMPANY_EMAIL': settings.COMPANY_EMAIL,
        'COMPANY_ADDRESS': settings.COMPANY_ADDRESS,
        'footer_services': Service.objects.filter(is_active=True)[:3],
        'SHOW_WORK_NAV': settings.SHOW_WORK_NAV,
        'SOCIAL_FACEBOOK_URL': settings.SOCIAL_FACEBOOK_URL,
        'SOCIAL_INSTAGRAM_URL': settings.SOCIAL_INSTAGRAM_URL,
    }
