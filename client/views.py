from datetime import datetime, date, time, timedelta
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy

from generic.models import Specialization, Clinic
from accounts.models import DoctorProfile
from doctor.models import DoctorWorkingHours, Appointment
from .forms import SelectDateForm, AppointmentForm

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
    if 'query' in request.GET:
        query = request.GET.get('query').split(' ')
        profiles = list()
        users = list()
        for q_item in query:
            profiles += (DoctorProfile.objects.filter(
                user__first_name__icontains=q_item))[:]
            profiles += (DoctorProfile.objects.filter(
                user__last_name__icontains=q_item))[:]
            profiles += (DoctorProfile.objects.filter(
                specialization__name__icontains=q_item))[:]
            profiles += (DoctorProfile.objects.filter(
                clinic__name__icontains=q_item))[:]

        unique_profiles = list(set(profiles))
        for p in unique_profiles:
            users.append(get_object_or_404(User, pk=p.user.id))

        return TemplateResponse(request, 'client/doctors.html', {
            'data': zip(users, unique_profiles),
        })
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
        'doc_user': user,
        'profile': profile,
        'clinic': clinic,
    })


def clinics(request):
    if 'query' in request.GET:
        query = request.GET.get('query').split(' ')
        _clinics = list()
        for q_item in query:
            _clinics += Clinic.objects.filter(
                specializations__name__icontains=q_item)[:]
            _clinics += Clinic.objects.filter(name__icontains=q_item)[:]
            _clinics += Clinic.objects.filter(address__icontains=q_item)[:]
        unique_clinics = list(set(_clinics))
        return TemplateResponse(request, 'client/clinics.html', {
            'clinics': unique_clinics,
        })

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


def get_context(user, profile, hours):
    select_date_form = SelectDateForm()
    appointment_form = AppointmentForm()

    context = {
        'doctor_user': user,
        'doctor_profile': profile,
        'appointments': Appointment.objects.filter(doctor_profile=profile,
                                                   start__gte=datetime.now()),
        'interval': hours.consultation_interval,
        'current_date': '',
        'select_date_form': select_date_form,
        'appointment_form': appointment_form,
        'monday': hours.monday_start.strftime(
            '%H:%M') + ' - ' + hours.monday_end.strftime('%H:%M'),
        'tuesday': hours.tuesday_start.strftime(
            '%H:%M') + ' - ' + hours.tuesday_end.strftime('%H:%M'),
        'wednesday': hours.wednesday_start.strftime(
            '%H:%M') + ' - ' + hours.wednesday_end.strftime('%H:%M'),
        'thursday': hours.thursday_start.strftime(
            '%H:%M') + ' - ' + hours.thursday_end.strftime('%H:%M'),
        'friday': hours.friday_start.strftime(
            '%H:%M') + ' - ' + hours.friday_end.strftime('%H:%M'),
        'saturday': hours.saturday_start.strftime(
            '%H:%M') + ' - ' + hours.saturday_end.strftime('%H:%M'),
        'sunday': hours.sunday_start.strftime(
            '%H:%M') + ' - ' + hours.sunday_end.strftime('%H:%M'),
    }
    return context


def add_delta(tme, delta):
    return (datetime.combine(date.today(), tme) +
            delta).time()


def make_datetime(my_date, my_time):
    return datetime.combine(my_date, my_time)


def schedule(request, doctor_pk):
    if request.method == 'POST':
        if 'select_date' in request.POST:
            select_date_form = SelectDateForm(request.POST)
            if select_date_form.is_valid():
                user = get_object_or_404(User, pk=doctor_pk)
                profile = get_object_or_404(DoctorProfile, user=user)
                hours = get_object_or_404(DoctorWorkingHours,
                                          doctor_profile=profile)
                context = get_context(user, profile, hours)

                current_date = select_date_form.cleaned_data['date']
                context['current_date'] = current_date.strftime('%Y-%m-%d')
                timestamps = list()
                booked = list()

                if current_date.weekday() == 0:  # monday

                    step = timedelta(minutes=hours.consultation_interval)
                    start = hours.monday_start
                    end = hours.monday_end
                    while start < end:
                        apps = Appointment.objects.filter(
                            start=make_datetime(current_date, start))
                        if not apps:
                            booked.append('free')
                        else:
                            booked.append('booked')
                        timestamps.append(start.strftime('%H:%M'))
                        start = add_delta(start, step)
                elif current_date.weekday() == 1:
                    step = timedelta(minutes=hours.consultation_interval)
                    start = hours.tuesday_start
                    end = hours.tuesday_end
                    while start < end:
                        apps = Appointment.objects.filter(
                            start=make_datetime(current_date, start))
                        if not apps:
                            booked.append('free')
                        else:
                            booked.append('booked')
                        timestamps.append(start.strftime('%H:%M'))
                        start = add_delta(start, step)
                elif current_date.weekday() == 2:
                    step = timedelta(minutes=hours.consultation_interval)
                    start = hours.wednesday_start
                    end = hours.wednesday_end
                    while start < end:
                        apps = Appointment.objects.filter(
                            start=make_datetime(current_date, start))
                        if not apps:
                            booked.append('free')
                        else:
                            booked.append('booked')
                        timestamps.append(start.strftime('%H:%M'))
                        start = add_delta(start, step)
                elif current_date.weekday() == 3:
                    step = timedelta(minutes=hours.consultation_interval)
                    start = hours.thursday_start
                    end = hours.thursday_end
                    while start < end:
                        apps = Appointment.objects.filter(
                            start=make_datetime(current_date, start))
                        if not apps:
                            booked.append('free')
                        else:
                            booked.append('booked')
                        timestamps.append(start.strftime('%H:%M'))
                        start = add_delta(start, step)
                elif current_date.weekday() == 4:
                    step = timedelta(minutes=hours.consultation_interval)
                    start = hours.friday_start
                    end = hours.friday_end
                    while start < end:
                        apps = Appointment.objects.filter(
                            start=make_datetime(current_date, start))
                        if not apps:
                            booked.append('free')
                        else:
                            booked.append('booked')
                        timestamps.append(start.strftime('%H:%M'))
                        start = add_delta(start, step)
                elif current_date.weekday() == 5:
                    step = timedelta(minutes=hours.consultation_interval)
                    start = hours.saturday_start
                    end = hours.saturday_end
                    while start < end:
                        apps = Appointment.objects.filter(
                            start=make_datetime(current_date, start))
                        if not apps:
                            booked.append('free')
                        else:
                            booked.append('booked')
                        timestamps.append(start.strftime('%H:%M'))
                        start = add_delta(start, step)
                elif current_date.weekday() == 6:  # sunday
                    step = timedelta(minutes=hours.consultation_interval)
                    start = hours.sunday_start
                    end = hours.sunday_end
                    while start < end:
                        apps = Appointment.objects.filter(
                            start=make_datetime(current_date, start))
                        if not apps:
                            booked.append('free')
                        else:
                            booked.append('booked')
                        timestamps.append(start.strftime('%H:%M'))
                        start = add_delta(start, step)

                context['appointments'] = zip(timestamps, booked)
                return TemplateResponse(request, 'client/schedule.html',
                                        context)

        if 'make_appointment' in request.POST:
            appointment_form = AppointmentForm(request.POST)
            if appointment_form.is_valid():
                appointment = appointment_form.save(commit=False)

                appointment.client = request.user
                # doctor_pk is the pk of a BaseUser
                user = get_object_or_404(User, pk=doctor_pk)
                profile = get_object_or_404(DoctorProfile, user=user)
                appointment.doctor_profile = profile
                appointment.save()
                return redirect(
                    reverse_lazy('client:appointment_success'))

    # doctor_pk is the pk of a BaseUser
    user = get_object_or_404(User, pk=doctor_pk)
    profile = get_object_or_404(DoctorProfile, user=user)
    hours = get_object_or_404(DoctorWorkingHours, doctor_profile=profile)

    return TemplateResponse(request, 'client/schedule.html',
                            get_context(user, profile, hours))


def appointments(request, client_pk):
    aps = Appointment.objects.filter(
        client=get_object_or_404(User, pk=client_pk),
        start__gte=datetime.now()).order_by('start')
    context = {
        'appointments': aps,
    }
    return TemplateResponse(request, 'client/appointments.html', context)


def appointment_success(request):
    return TemplateResponse(request, 'client/appointment_success.html', {})


def appointment_delete_confirm(request, pk):
    context = {
        'appointment': get_object_or_404(Appointment, pk=pk)
    }
    return TemplateResponse(request, 'client/appointment_delete_confirm.html',
                            context)


def appointment_delete(request, pk):
    get_object_or_404(Appointment, pk=pk).delete()
    return redirect('client:appointment_delete_done')


def appointment_delete_done(request):
    return TemplateResponse(request, 'client/appointment_delete_done.html', {})
