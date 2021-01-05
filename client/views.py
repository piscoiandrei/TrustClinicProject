from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from generic.models import Specialization, Clinic
from accounts.models import DoctorProfile

User = get_user_model()


def dashboard(request):
    data = Specialization.objects.all()
    if data:
        sps = data[:3]
    else:
        sps = None

    return TemplateResponse(request, 'client/dashboard.html', {
        'specializations': sps,
    })


def doctors(request):
    profiles = DoctorProfile.objects.all()[:]
    users = list()
    for p in profiles:
        users.append(get_object_or_404(User, pk=p.user.id))

    return TemplateResponse(request, 'client/doctors.html', {
        'data': zip(users, profiles),
    })


def doctor_detail(request, user_pk, profile_pk):
    user = get_object_or_404(User, pk=user_pk)
    profile = get_object_or_404(DoctorProfile, pk=profile_pk)
    clinic = get_object_or_404(Clinic, pk=profile.clinic.id)
    return TemplateResponse(request, 'client/doctor_detail.html', {
        'user': user,
        'profile': profile,
        'clinic': clinic,
    })


def clinics(request):
    _clinics = Clinic.objects.all()
    if _clinics:
        return TemplateResponse(request, 'client/clinics.html', {
            'clinics': _clinics,
        })
    else:
        raise Http404


def clinic_detail(request, pk):
    clinic = get_object_or_404(Clinic, pk=pk)
    sps = clinic.specializations.all()
    profiles = DoctorProfile.objects.filter(clinic=clinic)[:]
    users = list()
    for p in profiles:
        users.append(get_object_or_404(User, pk=p.user.id))
    return TemplateResponse(request, 'client/clinic_detail.html', {
        'clinic': clinic,
        'specializations': sps,
        'doctors': zip(users, profiles)
    })


def specializations(request):
    data = Specialization.objects.all()
    if data:
        sps = data
        return TemplateResponse(request, 'client/specializations.html', {
            'specializations': sps,
        })
    else:
        raise Http404


def specialization_detail(request, pk):
    specialization = get_object_or_404(Specialization, pk=pk)
    _clinics = Clinic.objects.filter(specializations=specialization)
    profiles = DoctorProfile.objects.filter(specialization=specialization)[:]
    users = list()
    for p in profiles:
        users.append(get_object_or_404(User, pk=p.user.id))

    return TemplateResponse(request, 'client/specialization_detail.html', {
        'specialization': specialization,
        'clinics': _clinics,
        'doctors': zip(users, profiles),
    })
