import django_filters
from dal import autocomplete
from contact.models import Contact


class ContactListFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(ContactListFilter, self).__init__(*args, **kwargs)

    last_name = django_filters.ChoiceFilter(
        choices=Contact.objects.all().values_list('last_name', 'last_name'),
        widget=autocomplete.ListSelect2(
            url='contact:last-name-autocomplete',
            attrs={'data-placeholder': 'Last name'}
        )
    )

    phone = django_filters.ChoiceFilter(
        choices=Contact.objects.all().values_list('phone__phone', 'phone__phone'),
        field_name='phone__phone',
        widget=autocomplete.ListSelect2(
            url='contact:phone-autocomplete',
            attrs={'data-placeholder': 'Phone'}
        )
    )

    email = django_filters.ChoiceFilter(
        choices=Contact.objects.all().values_list('email__email', 'email__email'),
        field_name='email__email',
        widget=autocomplete.ListSelect2(
            url='contact:email-autocomplete',
            attrs={'data-placeholder': 'E-mail'}
        )
    )

