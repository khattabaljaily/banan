from django.db import migrations

NEW_SERVICES = [
    dict(
        slug='website-development',
        icon='globe',
        order=2,
        name_en='Website Development',
        name_ar='تطوير المواقع الإلكترونية',
        summary_en='Professional business and marketing websites that represent your brand online.',
        summary_ar='مواقع إلكترونية احترافية للأعمال والتسويق تمثل علامتكم التجارية على الإنترنت.',
        description_en=(
            'We design and build fast, responsive websites — corporate sites, landing pages and '
            'portfolios — that load quickly, look sharp on every device, and are easy for your team '
            'to update. Built with SEO and accessibility in mind from the start.'
        ),
        description_ar=(
            'نصمم ونبني مواقع إلكترونية سريعة ومتجاوبة — مواقع الشركات، صفحات التسويق، ومعارض '
            'الأعمال — تُحمَّل بسرعة، وتظهر بشكل احترافي على جميع الأجهزة، ويسهل على فريقكم تحديثها. '
            'مبنية مع مراعاة تحسين محركات البحث وإمكانية الوصول منذ البداية.'
        ),
    ),
    dict(
        slug='technical-support',
        icon='support',
        order=6,
        name_en='Technical Support',
        name_ar='الدعم الفني',
        summary_en='Responsive day-to-day technical support to keep your team and systems running smoothly.',
        summary_ar='دعم فني يومي سريع الاستجابة لإبقاء فريقكم وأنظمتكم تعمل دون انقطاع.',
        description_en=(
            'From troubleshooting software issues to supporting your devices and network, our '
            'technical support team is on hand when something needs fixing. We offer remote and '
            'on-site support so problems get resolved quickly, with minimal disruption to your business.'
        ),
        description_ar=(
            'من حل مشكلات البرمجيات إلى دعم الأجهزة والشبكات، فريق الدعم الفني لدينا جاهز عند الحاجة. '
            'نقدّم الدعم عن بُعد وفي الموقع لضمان حل المشكلات بسرعة وبأقل قدر من التعطيل لأعمالكم.'
        ),
    ),
]

REORDER = {
    'custom-software-development': 1,
    'web-mobile-app-development': 3,
    'ecommerce-online-retail-solutions': 4,
    'it-consulting-managed-services': 5,
}


def add_services(apps, schema_editor):
    Service = apps.get_model('core', 'Service')
    for data in NEW_SERVICES:
        Service.objects.get_or_create(slug=data['slug'], defaults=data)
    for slug, order in REORDER.items():
        Service.objects.filter(slug=slug).update(order=order)


def remove_services(apps, schema_editor):
    Service = apps.get_model('core', 'Service')
    Service.objects.filter(slug__in=[s['slug'] for s in NEW_SERVICES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_seed_services'),
    ]

    operations = [
        migrations.RunPython(add_services, remove_services),
    ]
