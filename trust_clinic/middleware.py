from django.conf import settings
from django.urls import resolve
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class FooterDynamicData(MiddlewareMixin):

    # context_data should be added from a model, which is not defined yey
    def process_template_response(self, request, response):
        response.context_data['main_phone'] = '07n-amcartela'
        response.context_data['company_email'] = 'some@mail'
        response.context_data['creator_link'] = 'boss.com'
        return response


class LoginRequired(MiddlewareMixin):
    """
    Middleware for denying  user access to all pages except the ones from
    visitor namespace, extra functionality is subject to change
    """
    pass
