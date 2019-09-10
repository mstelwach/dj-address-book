from django.conf.urls import url

from contact.autocomplete import ContactLastNameAutocomplete, ContactPhoneAutocomplete, ContactEmailAutocomplete
from contact.views import *

app_name = 'contact'

urlpatterns = [
    url(r'^list/$', ContactListView.as_view(), name='list'),
    url(r'^create/$', ContactCreateView.as_view(), name='create'),
    url(r'^(?P<pk>[\d]+)/update/$', ContactUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[\d]+)/detail/$', ContactDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[\d]+)/delete/$', ContactDeleteView.as_view(), name='delete'),
    url(r'^(?P<pk>[\d]+)/phone/create/$', PhoneCreateView.as_view(), name='phone-create'),
    url(r'^(?P<pk>[\d]+)/phone/(?P<pk_2>[\d]+)/update/$', PhoneUpdateView.as_view(), name='phone-update'),
    url(r'^(?P<pk>[\d]+)/phone/(?P<pk_2>[\d]+)/delete/$', PhoneDeleteView.as_view(), name='phone-delete'),
    url(r'^(?P<pk>[\d]+)/email/create/$', EmailCreateView.as_view(), name='email-create'),
    url(r'^(?P<pk>[\d]+)/email/(?P<pk_2>[\d]+)/update/$', EmailUpdateView.as_view(), name='email-update'),
    url(r'^(?P<pk>[\d]+)/email/(?P<pk_2>[\d]+)/delete/$', EmailDeleteView.as_view(), name='email-delete'),
    url(r'^(?P<pk>[\d]+)/social-profile/create/$', SocialProfileCreateView.as_view(), name='social-profile-create'),
    url(r'^(?P<pk>[\d]+)/social-profile/(?P<pk_2>[\d]+)/update/$', SocialProfileUpdateView.as_view(),
        name='social-profile-update'),
    url(r'^(?P<pk>[\d]+)/social-profile/(?P<pk_2>[\d]+)/delete/$', SocialProfileDeleteView.as_view(),
        name='social-profile-delete'),
]

autocomplete_url_patterns = [
    url(r'^contact-last-name/autocomplete/$', ContactLastNameAutocomplete.as_view(), name='last-name-autocomplete'),
    url(r'^contact-phone/autocomplete/$', ContactPhoneAutocomplete.as_view(), name='phone-autocomplete'),
    url(r'^contact-email/autocomplete/$', ContactEmailAutocomplete.as_view(), name='email-autocomplete')

]

urlpatterns += autocomplete_url_patterns

