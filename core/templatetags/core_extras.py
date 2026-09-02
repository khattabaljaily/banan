import os

from django import template
from django.conf import settings
from django.templatetags.static import static as static_url
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def static_v(path):
    """Like {% static %} but appends ?v=<mtime> so browsers pick up
    edited CSS/JS immediately instead of serving a stale cached copy."""
    url = static_url(path)
    file_path = settings.BASE_DIR / 'static' / path
    try:
        version = int(os.path.getmtime(file_path))
    except OSError:
        version = 0
    separator = '&' if '?' in url else '?'
    return f'{url}{separator}v={version}'

_ICONS = {
    'code': '<path d="M8 4 2 12l6 8"/><path d="M16 4l6 8-6 8"/>',
    'cloud': '<path d="M7 18a4.5 4.5 0 0 1-.5-8.98A6 6 0 0 1 18 8.5a4 4 0 0 1-1 7.5H7Z"/>',
    'cart': '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/>'
            '<path d="M2.5 3h2.4l2.2 11.4a2 2 0 0 0 2 1.6h8a2 2 0 0 0 2-1.6L21 7H6.4"/>',
    'shield': '<path d="M12 3 4.5 6v6c0 4.6 3 7.9 7.5 9 4.5-1.1 7.5-4.4 7.5-9V6L12 3Z"/>'
              '<path d="m9.5 12 1.8 1.8L15 10"/>',
    'chart': '<path d="M4 20V10"/><path d="M12 20V4"/><path d="M20 20v-7"/>',
    'devices': '<rect x="3" y="4" width="14" height="10" rx="1.5"/>'
               '<path d="M8 20h6"/><path d="M11 14v6"/>'
               '<rect x="17" y="9" width="5" height="8" rx="1"/>',
    'check': '<path d="m5 13 4 4L19 7"/>',
    'arrow': '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    'pin': '<path d="M12 22s7-6.2 7-12A7 7 0 0 0 5 10c0 5.8 7 12 7 12Z"/><circle cx="12" cy="10" r="2.5"/>',
    'phone': '<path d="M4 5c0 8.3 6.7 15 15 15l2-4-5-2-2 2c-2-1-4-3-5-5l2-2-2-5-4 1Z"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    'quote': '<path d="M7 8c-2.2 0-4 1.8-4 4v4h6v-6H7Zm10 0c-2.2 0-4 1.8-4 4v4h6v-6h-2Z"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>'
             '<path d="M12 3c2.6 2.5 4 5.8 4 9s-1.4 6.5-4 9c-2.6-2.5-4-5.8-4-9s1.4-6.5 4-9Z"/>',
    'support': '<path d="M4 13v-1a8 8 0 0 1 16 0v1"/>'
               '<rect x="2.5" y="13" width="5" height="7" rx="2"/>'
               '<rect x="16.5" y="13" width="5" height="7" rx="2"/>'
               '<path d="M20 20a4 4 0 0 1-4 4h-2"/>',
    'facebook': '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    'instagram': '<rect x="2" y="2" width="20" height="20" rx="5"/>'
                 '<path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/>'
                 '<path d="M17.5 6.5h.01"/>',
    'box': '<path d="M21 8 12 3 3 8l9 5 9-5Z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/>',
    'wallet': '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18"/><circle cx="16.5" cy="14.5" r="1.1"/>',
    'register': '<rect x="4" y="4" width="16" height="11" rx="1.5"/><path d="M9 15v3M15 15v3"/><rect x="6.5" y="18" width="11" height="2.5" rx="1"/><path d="M8 8h8"/>',
    'store': '<path d="M4 9 5 4h14l1 5"/><path d="M4 9v11h16V9"/><path d="M9 20v-6h6v6"/>',
    'lock': '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    'sparkle': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4"/><path d="m6 6 2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>',
    'close': '<path d="M6 6l12 12M18 6 6 18"/>',
    'calendar': '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M8 3v4M16 3v4M3.5 10h17"/>',
    'users': '<circle cx="9" cy="8.5" r="3.3"/><path d="M3 20a6 6 0 0 1 12 0"/>'
             '<circle cx="17.5" cy="9.5" r="2.6"/><path d="M15.5 13.7A5 5 0 0 1 21 20"/>',
    'print': '<rect x="6" y="2.5" width="12" height="6.5" rx="1"/>'
             '<rect x="3.5" y="9" width="17" height="8" rx="1.5"/>'
             '<rect x="8" y="14" width="8" height="7" rx="1"/>',
}


@register.simple_tag
def icon(name, size=24, cls=''):
    path = _ICONS.get(name, _ICONS['code'])
    svg = (
        f'<svg class="icon {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="1.7" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'{path}</svg>'
    )
    return mark_safe(svg)
