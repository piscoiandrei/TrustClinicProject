from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
# Create your views here.
from django.template.response import TemplateResponse


def operator_session(request):
    request.session['operator'] = 'authorized'
    return redirect('chat:operator', pk=request.user.id)


def client_session(request):
    request.session['client'] = 'authorized'
    return redirect('chat:client', pk=request.user.id)


def operator(request, pk):
    if 'operator' in request.session:
        if request.session['operator'] == 'authorized':
            request.session['operator'] = 'denied'
            return TemplateResponse(request, 'chat/operator.html', {})

    raise PermissionDenied()


def client(request, pk):
    if 'client' in request.session:
        if request.session['client'] == 'authorized':
            request.session['client'] = 'denied'
            return TemplateResponse(request, 'chat/client.html', {})

    raise PermissionDenied()
