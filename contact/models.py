from django.core.validators import RegexValidator
from django.db import models
from account.models import Account


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    birth_year = models.DateField(null=True, blank=True)
    site_url = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return 'Account: {}  | First Name: {} | Last Name: {}'.format(self.account.username,
                                                                      self.first_name,
                                                                      self.last_name)


LABEL_PHONE = [
    ('home', 'Home'),
    ('work', 'Work'),
    ('mobile_phone', 'Mobile Phone'),
    ('primary', 'Primary'),
    ('pager', 'Pager')
]

only_numbers = RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')


class Phone(models.Model):
    person = models.ForeignKey(Contact, on_delete=models.CASCADE, editable=False)
    phone = models.CharField(max_length=50, validators=[only_numbers])
    label = models.CharField(max_length=16, choices=LABEL_PHONE, default=LABEL_PHONE[2][0])

    def __str__(self):
        return '{}'.format(self.phone)


LABEL_EMAIL = [
    ('home', 'Home'),
    ('work', 'Work'),
]


class Email(models.Model):
    person = models.ForeignKey(Contact, on_delete=models.CASCADE, editable=False)
    email = models.EmailField()
    label = models.CharField(max_length=16, choices=LABEL_EMAIL, default=LABEL_EMAIL[0][0])

    def __str__(self):
        return '{}'.format(self.email)


SOCIAL_PROFILES = [
    ('twitter', 'Twitter'),
    ('facebook', 'Facebook'),
    ('linkedin', 'Linkedin'),
    ('instagram', 'Instagram')
]


class SocialProfile(models.Model):
    person = models.ForeignKey(Contact, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=16, choices=SOCIAL_PROFILES)
    profile = models.CharField(max_length=50)

    def __str__(self):
        return '{} -- {}'.format(self.name, self.profile)




