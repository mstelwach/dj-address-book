import django_tables2 as tables
from django.utils.html import format_html

from contact.models import Contact, Phone, Email, SocialProfile


class ContactTable(tables.Table):
    actions = tables.TemplateColumn(template_name='contact/table_actions.html', verbose_name="Actions",
                                    orderable=False)
    phones = tables.Column(accessor='phone_set.all', orderable=False)
    emails = tables.Column(accessor='email_set.all', orderable=False)
    social_profiles = tables.Column(accessor='socialprofile_set.all', orderable=False)

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'birth_year', 'site_url', 'phones', 'emails', 'social_profiles', 'actions']

    def render_phones(self, record):
        phones = ', '.join([phone.phone for phone in record.phone_set.all()])
        return '{}'.format(phones)

    def render_emails(self, record):
        emails = ', '.join([email.email for email in record.email_set.all()])
        return '{}'.format(emails)

    def render_social_profiles(self, record):
        social_icon = '<a href="http://www.{}.com/{}"><i class="fa fa-fw fa-{}"></i></a>'
        social_profiles = ' '.join([social_icon.format(social_profile.name, social_profile.profile, social_profile.name)
                                    for social_profile in record.socialprofile_set.all()])
        return format_html(social_profiles)


class PhoneTable(tables.Table):
    actions = tables.TemplateColumn(template_name='contact/phone/table_actions.html', verbose_name="Actions",
                                    orderable=False)

    class Meta:
        model = Phone
        fields = ['phone', 'label', 'actions']


class EmailTable(tables.Table):
    actions = tables.TemplateColumn(template_name='contact/email/table_actions.html', verbose_name="Actions",
                                    orderable=False)

    class Meta:
        model = Email
        fields = ['email', 'label', 'actions']


class SocialProfileTable(tables.Table):
    actions = tables.TemplateColumn(template_name='contact/social_profile/table_actions.html', verbose_name="Actions",
                                    orderable=False)

    class Meta:
        model = SocialProfile
        fields = ['name', 'profile', 'actions']