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
    pass
