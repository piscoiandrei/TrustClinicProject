from django import forms
from .models import DoctorWorkingHours


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DoctorWorkingHoursForm(forms.ModelForm):
    class Meta:
        model = DoctorWorkingHours
        exclude = ['doctor_profile']
        widgets = {
            'monday_start': TimeInput(),
            'monday_end': TimeInput(),
            'tuesday_start': TimeInput(),
            'tuesday_end': TimeInput(),
            'wednesday_start': TimeInput(),
            'wednesday_end': TimeInput(),
            'thursday_start': TimeInput(),
            'thursday_end': TimeInput(),
            'friday_start': TimeInput(),
            'friday_end': TimeInput(),
            'saturday_start': TimeInput(),
            'saturday_end': TimeInput(),
            'sunday_start': TimeInput(),
            'sunday_end': TimeInput(),
        }
