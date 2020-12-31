from django.conf import settings
from django.urls import resolve
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from generic.models import FooterData


class FooterDynamicData(MiddlewareMixin):

    def process_template_response(self, request, response):
        f = FooterData.objects.values()[0]
        response.context_data['main_phone'] = f['phone']
        response.context_data['company_email'] = f['company_email']
        response.context_data['creator_link'] = f['creator_link']
        return response


class LoginRequired(MiddlewareMixin):
    """
    Middleware for denying  user access to all pages except the ones from
    visitor namespace, extra functionality is subject to change
    """
    # todo the login middleware should restrict access based on roles aswell
    pass
