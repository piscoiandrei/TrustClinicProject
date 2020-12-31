from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.template.response import TemplateResponse
from django.views.generic import UpdateView
from django.views.generic.edit import FormView, CreateView
from django.shortcuts import resolve_url
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model, \
    login as auth_login, update_session_auth_hash
from .forms import RegisterForm

User = get_user_model()


class Login(LoginView):
    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        user = self.request.user

        if user.is_authenticated:
            if user.is_operator:
                return redirect(
                    reverse_lazy('chat:operator_session'))
            if user.is_doctor:
                return redirect(
                    reverse_lazy('doctor:dashboard'))
            if user.is_staff or user.is_superuser:
                return redirect(resolve_url('/admin/'))
            if user.is_client:
                return redirect(
                    reverse_lazy('client:dashboard'))
        else:
            return redirect(resolve_url(settings.LOGIN_URL))


class EditProfile(UpdateView):
    model = User
    fields = ('email', 'first_name', 'last_name', 'phone', 'personal_id',)
    # template naming convention
    # <model_name>_<template_name_suffix>.html
    template_name_suffix = '_update_form'


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
