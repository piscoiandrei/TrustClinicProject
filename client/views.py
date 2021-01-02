from django.template.response import TemplateResponse
from generic.models import Specialization


def dashboard(request):
    data = Specialization.objects.all()
    if data:
        sps = data[:3]
    else:
        sps = None

    return TemplateResponse(request, 'client/dashboard.html', {
        'specializations': sps,
    })
