from django.db import migrations

PROJECT = dict(
    slug='banan-ims',
    title_en='Banan — Inventory & Sales Management Platform',
    title_ar='بنان — نظام إدارة المخزون والمبيعات',
    summary_en=(
        'An AI-powered, multi-tenant SaaS platform for inventory, sales, purchasing and finance — '
        'built in-house for retail, wholesale and service businesses, with an integrated online '
        'store and 36+ live reports.'
    ),
    summary_ar=(
        'نظام SaaS متكامل مدعوم بالذكاء الاصطناعي لإدارة المخزون والمبيعات والمشتريات والحسابات — '
        'من تطوير بنان الداخلي، مع متجر إلكتروني مدمج وأكثر من 36 تقريراً تحليلياً لحظياً.'
    ),
    description_en=(
        'Banan IMS is our own multi-tenant SaaS product — a full inventory, sales and '
        'business-management platform built from the ground up for retail, wholesale, food, '
        'pharmacy, electronics and service businesses across the Gulf and Arab markets.\n\n'
        'The platform covers the full operating cycle: multi-warehouse inventory with batch '
        'tracking and manufacturing/BOM support, point-of-sale and full sales invoicing with '
        'quotes and returns, purchasing with supplier RFQs, treasury and multi-account cash/bank '
        'management, expense tracking, and payroll with employee advances and a dedicated '
        'sales-delegate portal with commission tracking.\n\n'
        'Every subscriber also gets an instant, brandable online store with QR-code access, and '
        '36+ live analytical reports covering sales, inventory, customers and suppliers. An '
        'integrated AI assistant reads each business\'s real data to answer natural-language '
        'questions and generate daily health reports, and the whole interface is fully bilingual '
        '(Arabic/English) with 145 granular permissions per role, daily automated backups and '
        'end-to-end HTTPS encryption.'
    ),
    description_ar=(
        'بنان هو منتجنا الخاص القائم على SaaS — نظام متكامل لإدارة المخزون والمبيعات وعمليات '
        'الأعمال، مبني من الصفر لخدمة قطاعات التجزئة والجملة والمواد الغذائية والصيدليات '
        'والإلكترونيات والخدمات في السوق الخليجي والعربي.\n\n'
        'يغطي النظام دورة التشغيل الكاملة: مخازن متعددة مع تتبع الدفعات ودعم أوامر التصنيع '
        'وقوائم المكونات (BOM)، نقطة بيع وفواتير مبيعات كاملة مع عروض الأسعار والمرتجعات، '
        'مشتريات مع طلبات عروض أسعار من الموردين، خزائن وحسابات بنكية متعددة، تتبع مصروفات، '
        'وإدارة رواتب مع سلف الموظفين وبوابة مستقلة للمناديب مع تتبع العمولات.\n\n'
        'يحصل كل مشترك أيضاً على متجر إلكتروني فوري وقابل للتخصيص مع رمز QR، وأكثر من 36 '
        'تقريراً تحليلياً لحظياً يغطي المبيعات والمخزون والعملاء والموردين. يقرأ المساعد الذكي '
        'المدمج بيانات كل مشترك الفعلية للإجابة على الأسئلة وتوليد تقارير صحة الأعمال اليومية، '
        'والواجهة بالكامل ثنائية اللغة (عربي/إنجليزي) مع 145 صلاحية دقيقة لكل دور، ونسخ احتياطي '
        'يومي تلقائي، وتشفير HTTPS شامل.'
    ),
    image='portfolio/banan-ims-dashboard.png',
    is_featured=True,
    order=1,
)

SERVICE_SLUG = 'custom-software-development'


def add_project(apps, schema_editor):
    Service = apps.get_model('core', 'Service')
    Project = apps.get_model('core', 'Project')
    service = Service.objects.filter(slug=SERVICE_SLUG).first()
    Project.objects.get_or_create(
        slug=PROJECT['slug'],
        defaults={**PROJECT, 'service': service},
    )


def remove_project(apps, schema_editor):
    Project = apps.get_model('core', 'Project')
    Project.objects.filter(slug=PROJECT['slug']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_service_icon'),
    ]

    operations = [
        migrations.RunPython(add_project, remove_project),
    ]
