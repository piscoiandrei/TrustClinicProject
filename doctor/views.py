from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from .models import Appointment
from accounts.models import DoctorProfile
from .models import DoctorWorkingHours
from .forms import DoctorWorkingHoursForm
from datetime import datetime


def dashboard(request):
    context = {
        'appointments': Appointment.objects.filter(
            doctor_profile=get_object_or_404(DoctorProfile, user=request.user),
            start__gte=datetime.now()).order_by('start'),
        'hours_id': get_object_or_404(DoctorWorkingHours,
                                      doctor_profile=get_object_or_404(
                                          DoctorProfile, user=request.user)).id
    }
    return TemplateResponse(request, 'doctor/dashboard.html', context)


def appointment_delete(request, pk):
    get_object_or_404(Appointment, pk=pk).delete()
    return redirect('doctor:dashboard')


def hours_update(request, pk):
    hrs = get_object_or_404(DoctorWorkingHours,
                            doctor_profile=get_object_or_404(
                                DoctorProfile,
                                user=request.user))
    form = DoctorWorkingHoursForm(initial={
        'consultation_interval': hrs.consultation_interval,
        'monday_start': hrs.monday_start,
        'monday_end': hrs.monday_end,
        'tuesday_start': hrs.tuesday_start,
        'tuesday_end': hrs.tuesday_end,
        'wednesday_start': hrs.wednesday_start,
        'wednesday_end': hrs.wednesday_end,
        'thursday_start': hrs.thursday_start,
        'thursday_end': hrs.thursday_end,
        'friday_start': hrs.friday_start,
        'friday_end': hrs.friday_end,
        'saturday_start': hrs.saturday_start,
        'saturday_end': hrs.saturday_end,
        'sunday_start': hrs.sunday_start,
        'sunday_end': hrs.sunday_end,
    })
    context = {
        'hours_id': hrs.id,
        'form': form
    }
    return TemplateResponse(request, 'doctor/working_hours.html', context)
