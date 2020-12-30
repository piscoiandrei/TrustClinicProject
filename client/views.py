from django.template.response import TemplateResponse
from django.http import HttpResponse


def dashboard(request):
    return TemplateResponse(request, 'client/dashboard.html', {})
