from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def operator(request, pk):
    return HttpResponse('chat Operator view')


def client(request, pk):
    return HttpResponse('chat client view')
