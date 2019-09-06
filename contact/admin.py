from django.contrib import admin
from contact.models import Contact, Phone, Email


class PhoneInline(admin.StackedInline):
    model = Phone


class EmailInline(admin.StackedInline):
    model = Email


class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'account']
    inlines = [PhoneInline, EmailInline]


admin.site.register(Contact, ContactAdmin)
