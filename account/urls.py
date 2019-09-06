from django.conf.urls import url

from account.views import *

app_name = 'account'

urlpatterns = [
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^create/$', AccountCreateView.as_view(), name='create'),
    url(r'^detail/$', AccountDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[\d]+)/update/$', AccountUpdateView.as_view(), name='update'),
    url(r'^password/change/$', AccountPasswordChangeView.as_view(), name='password-change'),
    url(r'^password/reset/$', AccountPasswordResetView.as_view(), name='password-reset'),
    url(r'^password/reset/done/$', AccountPasswordResetDoneView.as_view(), name='password-reset-done'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        AccountPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    url(r'^password/reset/done/$', AccountPasswordResetCompleteView.as_view(), name='password-reset-complete'),

]