from django.contrib import admin

from .models import ContactMessage, Project, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ar', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name_en',)}
    search_fields = ('name_en', 'name_ar')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_ar', 'service', 'is_featured', 'order')
    list_editable = ('order', 'is_featured')
    prepopulated_fields = {'slug': ('title_en',)}
    search_fields = ('title_en', 'title_ar')
    list_filter = ('service', 'is_featured')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
