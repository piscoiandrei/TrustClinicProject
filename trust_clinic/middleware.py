from django.conf import settings
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
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

    def match_path(self, path, urls):
        for url in urls:
            if path in url or path == url:
                return True
            if url in path:
                return True
        return False

    def match_all(self, path):
        if self.match_path(path, settings.CLIENT_URLS):
            return True
        if self.match_path(path, settings.OPERATOR_URLS):
            return True
        if self.match_path(path, settings.DOCTOR_URLS):
            return True
        return False

    def redirect_role(self, user):
        if user.is_operator:
            return redirect('chat:operator_session')
        if user.is_doctor:
            return redirect('doctor:dashboard')
        if user.is_staff or user.is_superuser:
            return redirect(resolve_url('/admin/'))
        if user.is_client:
            return redirect('client:dashboard')

    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path
        user = request.user

        if not user.is_authenticated:
            if not self.match_path(path=path,
                                   urls=settings.LOGGED_OUT_ONLY_URLS):
                return redirect('visitor:home')
            if path == '/':
                return redirect('visitor:home')

        if user.is_authenticated:
            if self.match_path(path=path, urls=settings.LOGGED_OUT_ONLY_URLS):
                self.redirect_role(user)

            if not self.match_path(path=path,
                                   urls=settings.LOGIN_REQUIRED_URLS):
                if user.is_client:
                    if not self.match_path(path=path,
                                           urls=settings.CLIENT_URLS):
                        return redirect('client:dashboard')

                if user.is_operator:
                    if not self.match_path(path=path,
                                           urls=settings.OPERATOR_URLS):
                        return redirect('chat:operator_session')

                if user.is_doctor:
                    if not self.match_path(path=path,
                                           urls=settings.DOCTOR_URLS):
                        return redirect('doctor:dashboard')

                if user.is_staff or user.is_superuser:
                    if self.match_all(path=path):
                        return redirect(resolve_url('/admin/'))
