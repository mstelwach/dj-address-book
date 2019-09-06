from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin

from contact.models import Contact


class ContactLastNameAutocomplete(LoginRequiredMixin, autocomplete.Select2ListView):

    def get_list(self):
        queryset = Contact.objects.filter(account=self.request.user)
        queryset = list(queryset.values_list('last_name', flat=True))
        queryset.append(self.q)
        return queryset


class ContactPhoneAutocomplete(LoginRequiredMixin, autocomplete.Select2ListView):

    def get_list(self):
        queryset = Contact.objects.filter(account=self.request.user)
        queryset = list(queryset.values_list('phone__phone', flat=True))
        queryset.append(self.q)
        return queryset


class ContactEmailAutocomplete(LoginRequiredMixin, autocomplete.Select2ListView):

    def get_list(self):
        queryset = Contact.objects.filter(account=self.request.user)
        queryset = list(queryset.values_list('email__email', flat=True))
        queryset.append(self.q)
        return queryset

