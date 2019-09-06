from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from account.forms import AccountCreateForm, AccountUpdateForm
from account.models import Account


class Login(LoginView):
    template_name = 'account/login.html'
    form_class = AuthenticationForm


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'


class AccountCreateView(SuccessMessageMixin, CreateView):
    template_name = 'account/create.html'
    form_class = AccountCreateForm
    success_url = reverse_lazy('login')
    success_message = "Your account was created successfully."


class AccountDetailView(LoginRequiredMixin, DetailView):
    template_name = 'account/detail.html'

    def get_object(self, queryset=None):
        return self.request.user


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    template_name = 'account/update.html'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('account:detail')
    success_message = "Your account was updated successfully."

    def form_valid(self, form):
        return super(AccountUpdateView, self).form_valid(form)


class AccountPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = "account/password_change.html"
    success_url = reverse_lazy('account:detail')
    success_message = "The passwords was changed successfully."


class AccountPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')


class AccountPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'
    success_url = reverse_lazy('profiles:password_reset_complete')


class AccountPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('profiles:password_reset_complete')


class AccountPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'
