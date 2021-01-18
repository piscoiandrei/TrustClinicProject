from django.template.response import TemplateResponse


def dashboard(request):
    return TemplateResponse(request, 'doctor/dashboard.html', {})
