from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.response import TemplateResponse


def operator(request, pk):
    return TemplateResponse(request, 'chat/operator.html', {})


def client(request, pk):
    return TemplateResponse(request, 'chat/client.html', {})
