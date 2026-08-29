from django.db import migrations

SERVICES = [
    dict(
        slug='custom-software-development',
        icon='code',
        order=1,
        name_en='Custom Software Development',
        name_ar='تطوير البرمجيات المخصصة',
        summary_en='Bespoke software designed and programmed around the way your business actually works.',
        summary_ar='برمجيات مصممة ومبرمجة خصيصًا لتناسب طريقة عمل مؤسستك.',
        description_en=(
            'We design and build custom software from the ground up — internal tools, business systems, '
            'APIs and automations — using modern, maintainable technology. Every engagement starts with '
            'understanding your workflow, then translating it into software that removes friction instead '
            'of adding it. We stay involved after launch to support, extend and improve what we build.'
        ),
        description_ar=(
            'نقوم بتصميم وبرمجة حلول برمجية مخصصة من الصفر — أدوات داخلية، أنظمة أعمال، واجهات برمجية '
            'وأتمتة للعمليات — باستخدام تقنيات حديثة وقابلة للصيانة. نبدأ كل مشروع بفهم طريقة عملكم فعليًا، '
            'ثم نترجم ذلك إلى برمجيات تُسهّل العمل بدلاً من تعقيده. ونستمر في دعم وتطوير ما نبنيه بعد الإطلاق.'
        ),
    ),
    dict(
        slug='web-mobile-app-development',
        icon='devices',
        order=2,
        name_en='Web & Mobile Application Development',
        name_ar='تطوير تطبيقات الويب والجوال',
        summary_en='Fast, modern websites and mobile apps built to convert visitors into customers.',
        summary_ar='مواقع وتطبيقات جوال حديثة وسريعة مصممة لتحويل الزوار إلى عملاء.',
        description_en=(
            'From marketing websites to full web and mobile applications, we build interfaces that are fast, '
            'accessible and easy to maintain. We work across the stack — front end, back end and deployment '
            '— and design in both Arabic and English so your product feels native to every visitor.'
        ),
        description_ar=(
            'من المواقع التعريفية إلى تطبيقات الويب والجوال المتكاملة، نبني واجهات سريعة وسهلة الاستخدام '
            'وقابلة للصيانة. نعمل على كامل الطبقات التقنية — الواجهة الأمامية والخلفية والنشر — ونصمم '
            'بالعربية والإنجليزية ليشعر كل زائر أن المنتج مصمم له خصيصًا.'
        ),
    ),
    dict(
        slug='ecommerce-online-retail-solutions',
        icon='cart',
        order=3,
        name_en='E-commerce & Online Retail Solutions',
        name_ar='حلول التجارة الإلكترونية والبيع بالتجزئة',
        summary_en='Online stores and order-management systems built to sell, from checkout to fulfillment.',
        summary_ar='متاجر إلكترونية وأنظمة إدارة طلبات مصممة للبيع، من الدفع حتى التسليم.',
        description_en=(
            'We build online retail experiences that make it easy for customers to browse, buy and come back. '
            'That includes storefronts, payment integration, order and inventory management, and the '
            'back-office tools your team needs to run an online business day to day.'
        ),
        description_ar=(
            'نبني تجارب بيع إلكتروني تُسهّل على العملاء التصفح والشراء والعودة مجددًا. يشمل ذلك واجهات '
            'المتاجر، ربط بوابات الدفع، إدارة الطلبات والمخزون، وأدوات الإدارة اليومية التي يحتاجها '
            'فريقكم لتشغيل متجر إلكتروني ناجح.'
        ),
    ),
    dict(
        slug='it-consulting-managed-services',
        icon='cloud',
        order=4,
        name_en='IT Consulting & Managed Services',
        name_ar='استشارات وخدمات تقنية المعلومات المُدارة',
        summary_en='Practical IT guidance and ongoing support so your systems stay reliable as you grow.',
        summary_ar='استشارات تقنية عملية ودعم مستمر لضمان استقرار أنظمتكم مع نمو أعمالكم.',
        description_en=(
            'Not every business needs a full internal IT department. We provide consulting and managed '
            'support — infrastructure planning, software selection, systems setup and ongoing technical '
            'support — so you get senior-level guidance without the overhead.'
        ),
        description_ar=(
            'ليست كل الشركات بحاجة إلى قسم تقني داخلي متكامل. نقدّم استشارات وخدمات دعم مُدارة — تخطيط '
            'البنية التقنية، اختيار البرمجيات المناسبة، إعداد الأنظمة والدعم الفني المستمر — لتحصلوا على '
            'خبرة تقنية عالية دون أعباء إضافية.'
        ),
    ),
]


def seed_services(apps, schema_editor):
    Service = apps.get_model('core', 'Service')
    for data in SERVICES:
        Service.objects.get_or_create(slug=data['slug'], defaults=data)


def remove_services(apps, schema_editor):
    Service = apps.get_model('core', 'Service')
    Service.objects.filter(slug__in=[s['slug'] for s in SERVICES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_services, remove_services),
    ]
