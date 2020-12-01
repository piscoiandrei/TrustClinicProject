from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateResponse


def home(request):
    return TemplateResponse(request, 'visitor/home.html', {})


# this should redirected to the unexisting login page, handled by another app
def login_redirect(request):
    return redirect('/')
