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

    def match_path(self, path, urls):
        for url in urls:
            if path in url or path == url:
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

    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path
        user = request.user
