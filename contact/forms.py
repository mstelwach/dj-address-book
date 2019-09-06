from django import forms

from contact.models import Contact


class ContactCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ['account', 'date']

