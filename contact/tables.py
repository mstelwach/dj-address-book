import django_tables2 as tables

from contact.models import Contact, Phone, Email


class ContactTable(tables.Table):
    actions = tables.TemplateColumn(template_name='contact/table_actions.html', verbose_name="Actions",
                                    orderable=False)

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'actions']


class PhoneTable(tables.Table):
    actions = tables.TemplateColumn(template_name='contact/phone/table_actions.html', verbose_name="Actions",
                                    orderable=False)

    class Meta:
        model = Phone
        fields = ['phone', 'actions']


class EmailTable(tables.Table):
    actions = tables.TemplateColumn(template_name='contact/email/table_actions.html', verbose_name="Actions",
                                    orderable=False)

    class Meta:
        model = Email
        fields = ['email', 'actions']

