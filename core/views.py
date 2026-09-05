from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import translate_url
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, TemplateView

from .forms import ContactForm, WebsiteRequestForm
from .models import Project, Service


def set_language_redirect(request, lang_code):
    """GET-based language switch that keeps the visitor on the same page."""
    if lang_code not in dict(settings.LANGUAGES):
        lang_code = settings.LANGUAGE_CODE
    referer = request.META.get('HTTP_REFERER')
    source_path = referer if referer else '/'
    path = translate_url(source_path, lang_code)
    response = redirect(path)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['services'] = Service.objects.filter(is_active=True)[:6]
        # Banan IMS has its own dedicated product page, not a "Work" case study.
        ctx['featured_projects'] = Project.objects.filter(is_featured=True).exclude(slug='banan-ims')[:3]
        return ctx


class AboutView(TemplateView):
    template_name = 'core/about.html'


class BananIMSProductView(TemplateView):
    template_name = 'core/product_banan_ims.html'


class BananBCMSProductView(TemplateView):
    template_name = 'core/product_banan_bcms.html'


class ProductsIndexView(TemplateView):
    template_name = 'core/products.html'


class ServiceListView(ListView):
    model = Service
    template_name = 'core/services.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(is_active=True)


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'core/service_detail.html'
    context_object_name = 'service'

    def get_queryset(self):
        return Service.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['related_projects'] = self.object.projects.all()[:6]
        return ctx


class PortfolioListView(ListView):
    model = Project
    template_name = 'core/portfolio.html'
    context_object_name = 'projects'

    def get_queryset(self):
        # Banan IMS has its own dedicated product page, not a "Work" case study.
        return Project.objects.exclude(slug='banan-ims')


class PortfolioDetailView(DetailView):
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'


class WebsiteRequestView(TemplateView):
    template_name = 'core/website_request.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('form', WebsiteRequestForm())
        return ctx

    def post(self, request, *args, **kwargs):
        form = WebsiteRequestForm(request.POST)
        if form.is_valid():
            website_request = form.save()
            self._notify(website_request)
            messages.success(
                request,
                _('Thank you! Your project brief has been received — our team will get back to you shortly.'),
            )
            return redirect('core:website_request')
        return self.render_to_response(self.get_context_data(form=form))

    def _notify(self, website_request):
        try:
            body = render_to_string('core/email/website_request_notification.txt', {'req': website_request})
            send_mail(
                subject=f'New website design request: {website_request.name}',
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL_RECIPIENT],
                fail_silently=True,
            )
        except Exception:
            pass


class ContactView(TemplateView):
    template_name = 'core/contact.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('form', ContactForm())
        return ctx

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            self._notify(contact_message)
            messages.success(
                request,
                _('Thank you! Your message has been received — our team will get back to you shortly.'),
            )
            return redirect('core:contact')
        return self.render_to_response(self.get_context_data(form=form))

    def _notify(self, contact_message):
        try:
            body = render_to_string('core/email/contact_notification.txt', {'msg': contact_message})
            send_mail(
                subject=f'New website inquiry: {contact_message.subject or contact_message.name}',
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL_RECIPIENT],
                fail_silently=True,
            )
        except Exception:
            pass
