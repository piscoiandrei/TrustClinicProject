from django.conf import settings
from django.shortcuts import render, resolve_url
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model, \
    login as auth_login


class Login(LoginView):
    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        user = self.request.user

        if user.is_authenticated:
            if user.is_operator:
                return redirect(
                    reverse_lazy('chat:operator', kwargs={'pk': user.id}))
            if user.is_doctor:
                return redirect(
                    reverse_lazy('doctor:dashboard'))
            if user.is_staff or user.is_superuser:
                return redirect(resolve_url('/admin/'))
            else:
                return redirect(
                    reverse_lazy('client:dashboard'))
        else:
            return redirect(resolve_url(settings.LOGIN_URL))
