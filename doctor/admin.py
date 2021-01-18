from django.contrib import admin
from .models import *


class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment
    list_display = ['start', 'client_name', 'doctor_name']

    def client_name(self, obj):
        return obj.client.full_name

    client_name.short_description = 'Appointee'

    def doctor_name(self, obj):
        return obj.doctor_profile.user.full_name
    doctor_name.short_description = 'Doctor'


admin.site.register(DoctorWorkingHours)
admin.site.register(Appointment, AppointmentAdmin)
