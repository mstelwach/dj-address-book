from django.db import models
from account.models import Account


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return 'Account: {}  | First Name: {} | Last Name: {}'.format(self.account.username,
                                                                      self.first_name,
                                                                      self.last_name)


class Phone(models.Model):
    person = models.ForeignKey(Contact, on_delete=models.CASCADE, editable=False)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.phone)


class Email(models.Model):
    person = models.ForeignKey(Contact, on_delete=models.CASCADE, editable=False)
    email = models.EmailField()

    def __str__(self):
        return '{}'.format(self.email)

