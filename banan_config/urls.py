from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import set_language_redirect

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('set-language/<str:lang_code>/', set_language_redirect, name='set_language_redirect'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
