from django.db import migrations

PROJECTS = [
    dict(
        slug='banan-store',
        title_en='Banan Store — Online Marketplace',
        title_ar='بنان ستور — متجر إلكتروني',
        summary_en=(
            'A public online marketplace with catalog browsing, secure checkout and multiple '
            'payment options, built and hosted end to end.'
        ),
        summary_ar=(
            'متجر إلكتروني عام يتيح تصفح المنتجات والدفع الآمن بعدة وسائل، من التطوير إلى الاستضافة.'
        ),
        description_en=(
            'Banan Store is a live online marketplace we designed and built — covering product '
            'catalog and categories, search, user accounts, secure checkout and multiple payment '
            'and delivery options, ready for real customers from day one.'
        ),
        description_ar=(
            'بنان ستور هو متجر إلكتروني عام قمنا بتصميمه وبنائه — يشمل كتالوج المنتجات والتصنيفات، '
            'البحث، حسابات المستخدمين، الدفع الآمن، وخيارات متعددة للدفع والتوصيل، وجاهز لاستقبال '
            'العملاء الحقيقيين منذ اليوم الأول.'
        ),
        image='portfolio/bananstore-home.png',
        external_url='https://bananstore.online',
        is_featured=True,
        order=2,
    ),
    dict(
        slug='misfound',
        title_en='Misfound — Lost & Found Platform',
        title_ar='مِسفاوند — منصة المفقودات والموجودات',
        summary_en=(
            'A bilingual community platform connecting people who lost items with people who found '
            'them, across hundreds of Arab cities.'
        ),
        summary_ar=(
            'منصة مجتمعية ثنائية اللغة تربط بين من فقد شيئاً ومن وجده، في مئات المدن العربية.'
        ),
        description_en=(
            'Misfound is a bilingual (Arabic/English) lost-and-found platform that lets people post '
            'and search lost or found item reports, browse by category and country, and connect '
            'safely and directly with the other party — built and run as a public service.'
        ),
        description_ar=(
            'مِسفاوند منصة ثنائية اللغة (عربي/إنجليزي) للمفقودات والموجودات، تتيح للمستخدمين نشر '
            'والبحث عن بلاغات المفقودات أو الموجودات، والتصفح حسب التصنيف والدولة، والتواصل المباشر '
            'والآمن مع الطرف الآخر — تم تطويرها وتشغيلها كخدمة عامة.'
        ),
        image='portfolio/misfound-home.png',
        external_url='https://misfound.com',
        is_featured=True,
        order=3,
    ),
]

SERVICE_SLUG = 'website-development'


def add_projects(apps, schema_editor):
    Service = apps.get_model('core', 'Service')
    Project = apps.get_model('core', 'Project')
    service = Service.objects.filter(slug=SERVICE_SLUG).first()
    for data in PROJECTS:
        Project.objects.get_or_create(
            slug=data['slug'],
            defaults={**data, 'service': service},
        )


def remove_projects(apps, schema_editor):
    Project = apps.get_model('core', 'Project')
    Project.objects.filter(slug__in=[p['slug'] for p in PROJECTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_seed_banan_project'),
    ]

    operations = [
        migrations.RunPython(add_projects, remove_projects),
    ]
