from django.conf import settings
from django.urls import resolve, reverse_lazy
import re
from django.conf import settings
from django.shortcuts import redirect, resolve_url
from django.utils.deprecation import MiddlewareMixin
from generic.models import FooterData


class FooterDynamicData(MiddlewareMixin):

    def process_template_response(self, request, response):
        if 'admin' not in request.path:
            data = FooterData.objects.all()
            if data:
                f = data.values()[0]
                response.context_data['main_phone'] = f['phone']
                response.context_data['company_email'] = f['company_email']
                response.context_data['creator_link'] = f['creator_link']

        return response


class LoginRequired(MiddlewareMixin):

    def contains_ignored(self, path):
        for url in settings.IGNORE_LOGIN_REQUIRED:
            if url in path:
                return True
        return False

    def redirect_role(self, user):
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

    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path_info
        if request.user.is_authenticated:
            if ('client' in path) and (request.user.is_client == False):
                return self.redirect_role(request.user)
            elif ('operator' in path) and (request.user.is_operator == False):
                return self.redirect_role(request.user)
            elif ('doctor' in path) and (request.user.is_doctor == False):
                return self.redirect_role(request.user)
            elif ('operator' in path) and ((request.user.is_staff == False) or (
                    request.user.is_superuser == False)):
                return self.redirect_role(request.user)
        else:
            if path == '':
                return redirect('visitor:home')
            if not self.contains_ignored(path):
                return redirect('accounts:login')
