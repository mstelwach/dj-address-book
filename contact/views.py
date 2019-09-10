from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django_tables2 import RequestConfig

from contact.filters import ContactListFilter
from contact.forms import ContactCreateUpdateForm, PhoneCreateUpdateForm, EmailCreateUpdateForm, \
    SocialProfileCreateUpdateForm
from contact.helpers import get_phones_or_emails_string
from contact.models import Contact, Phone, Email, SocialProfile
from contact.tables import ContactTable, PhoneTable, EmailTable, SocialProfileTable


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contact/list.html'
    table_class = ContactTable
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        kwargs['user'] = self.request.user
        return super(ContactListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Contact.objects.filter(account=self.request.user)

    def filter_data(self, context):
        filtered_data = ContactListFilter(self.request.GET, queryset=self.get_queryset())
        context['filtered_data'] = filtered_data
        filtered_contact_table = self.table_class(data=filtered_data.qs, template_name="django_tables2/bootstrap4.html")
        return filtered_contact_table

    def get_context_data(self, **kwargs):
        context = super(ContactListView, self).get_context_data(**kwargs)
        contact_table = self.filter_data(context)
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(contact_table)
        context['contact_table'] = contact_table
        context['full_url'] = self.request.path
        return context


class ContactCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactCreateUpdateForm
    template_name = 'contact/create.html'
    success_message = 'The contact record was created successfully.'

    def get_success_url(self):
        if self.request.POST.get('save'):
            return reverse_lazy('contact:list')
        else:
            return reverse_lazy('contact:create')

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super(ContactCreateView, self).form_valid(form)


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'contact/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContactDetailView, self).get_context_data(**kwargs)
        contact = self.object
        context['phones'] = get_phones_or_emails_string(Phone, contact, 'phone')
        context['emails'] = get_phones_or_emails_string(Email, contact, 'email')
        context['social_profiles'] = ', '.join(contact.socialprofile_set.all())
        return context


class ContactUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contact
    form_class = ContactCreateUpdateForm
    template_name = "contact/update.html"
    success_url = reverse_lazy('contact:list')
    success_message = "The contact record was updated successfully."

    def form_valid(self, form):
        return super(ContactUpdateView, self).form_valid(form)

    # Phone and Email List View
    def get_context_data(self, **kwargs):
        context = super(ContactUpdateView, self).get_context_data(**kwargs)
        qs_phone = Phone.objects.filter(person=self.object)
        qs_email = Email.objects.filter(person=self.object)
        qs_social_profile = SocialProfile.objects.filter(person=self.object)
        phone_table = PhoneTable(data=qs_phone, template_name="django_tables2/bootstrap4.html", prefix='1-')
        email_table = EmailTable(data=qs_email, template_name="django_tables2/bootstrap4.html", prefix='2-')
        social_profile_table = SocialProfileTable(data=qs_social_profile, template_name="django_tables2/bootstrap4.html", prefix='3-')
        RequestConfig(self.request, paginate=False).configure(phone_table)
        RequestConfig(self.request, paginate=False).configure(email_table)
        RequestConfig(self.request, paginate=False).configure(social_profile_table)
        context['phone_table'] = phone_table
        context['email_table'] = email_table
        context['social_profile_table'] = social_profile_table
        return context


class ContactDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('contact:list')
    success_message = 'The contact record was deleted successfully.'

    def get(self, request, *args, **kwargs):
        contact = self.get_object()
        phones = contact.phone_set.values_list('phone', flat=True)
        emails = contact.email_set.values_list('email', flat=True)
        if phones or emails:
            messages.success(request, "Can't be deleted! The contact has phones or e-mails.")
            return HttpResponseRedirect(self.success_url)
        messages.success(request, self.success_message)
        return self.post(request, *args, **kwargs)


class PhoneCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Phone
    form_class = PhoneCreateUpdateForm
    template_name = 'contact/phone/create.html'
    success_message = "The phone record was created successfully."

    def get_success_url(self):
        pk = self.kwargs['pk']
        if self.request.POST.get('save'):
            return reverse_lazy('contact:update', kwargs={'pk': pk})
        else:
            return reverse_lazy('contact:phone-create', kwargs={'pk': pk})

    def form_valid(self, form):
        contact = Contact.objects.get(pk=self.kwargs['pk'])
        phone = form.save(commit=False)
        phone.person = contact
        phone.save()
        return super(PhoneCreateView, self).form_valid(form)


class PhoneUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Phone
    form_class = PhoneCreateUpdateForm
    template_name = 'contact/phone/update.html'
    success_message = "The phone record was updated successfully."

    def get_object(self, **kwargs):
        obj = Phone.objects.get(pk=self.kwargs.get('pk_2'))
        return obj

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('contact:update', kwargs={'pk': pk})

    def form_valid(self, form):
        form.instance.person = Contact.objects.get(pk=self.kwargs.get('pk'))
        return super(PhoneUpdateView, self).form_valid(form)


class PhoneDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Phone
    success_message = 'The phone record was deleted successfully.'

    def get_object(self, **kwargs):
        obj = Phone.objects.get(pk=self.kwargs.get('pk_2'))
        return obj

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('contact:update', kwargs={'pk': pk})

    def get(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return self.post(request, *args, **kwargs)


class EmailCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Email
    form_class = EmailCreateUpdateForm
    template_name = 'contact/email/create.html'
    success_message = "The e-mail record was created successfully."

    def get_success_url(self):
        pk = self.kwargs['pk']
        if self.request.POST.get('save'):
            return reverse_lazy('contact:update', kwargs={'pk': pk})
        else:
            return reverse_lazy('contact:email-create', kwargs={'pk': pk})

    def form_valid(self, form):
        form.instance.person = Contact.objects.get(pk=self.kwargs['pk'])
        return super(EmailCreateView, self).form_valid(form)


class EmailUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Email
    form_class = EmailCreateUpdateForm
    template_name = 'contact/email/update.html'
    success_message = "The e-mail record was updated successfully."

    def get_object(self, **kwargs):
        obj = Email.objects.get(pk=self.kwargs.get('pk_2'))
        return obj

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('contact:update', kwargs={'pk': pk})

    def form_valid(self, form):
        form.instance.person = Contact.objects.get(pk=self.kwargs.get('pk'))
        return super(EmailUpdateView, self).form_valid(form)


class EmailDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Email
    success_message = 'The e-mail record was deleted successfully.'

    def get_object(self, **kwargs):
        obj = Email.objects.get(pk=self.kwargs.get('pk_2'))
        return obj

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('contact:update', kwargs={'pk': pk})

    def get(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return self.post(request, *args, **kwargs)


class SocialProfileCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SocialProfile
    form_class = SocialProfileCreateUpdateForm
    template_name = 'contact/social_profile/create.html'
    success_message = "The social profile record was created successfully."

    def get_success_url(self):
        pk = self.kwargs['pk']
        if self.request.POST.get('save'):
            return reverse_lazy('contact:update', kwargs={'pk': pk})
        else:
            return reverse_lazy('contact:social-profile-create', kwargs={'pk': pk})

    def form_valid(self, form):
        form.instance.person = Contact.objects.get(pk=self.kwargs['pk'])
        return super(SocialProfileCreateView, self).form_valid(form)


class SocialProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SocialProfile
    form_class = SocialProfileCreateUpdateForm
    template_name = 'contact/social_profile/update.html'
    success_message = 'The social profile record was updated successfully.'

    def get_object(self, **kwargs):
        obj = SocialProfile.objects.get(pk=self.kwargs.get('pk_2'))
        return obj

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('contact:update', kwargs={'pk': pk})

    def form_valid(self, form):
        form.instance.person = Contact.objects.get(pk=self.kwargs['pk'])
        return super(SocialProfileUpdateView, self).form_valid(form)


class SocialProfileDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SocialProfile
    success_message = 'The social profile record was deleted successfully.'

    def get_object(self, **kwargs):
        obj = SocialProfile.objects.get(pk=self.kwargs.get('pk_2'))
        return obj

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('contact:update', kwargs={'pk': pk})

    def get(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return self.post(request, *args, **kwargs)
