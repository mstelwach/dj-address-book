from django import forms

from contact.models import Contact, Phone, Email, SocialProfile


class ContactCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ['account', 'date']
        widgets = {
            'birth_year': forms.DateInput(attrs={
                'id': 'datepicker'
            })
        }


class PhoneCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Phone
        exclude = ['person']


class EmailCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Email
        exclude = ['person']


class SocialProfileCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = SocialProfile
        exclude = ['person']
