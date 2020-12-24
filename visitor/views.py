from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponse


def home(request):
    return TemplateResponse(request, 'visitor/home.html', {})


def login_redirect(request):
    # add extra request request if needed
    return redirect(reverse_lazy('accounts:login'))
