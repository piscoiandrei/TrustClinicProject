from django import forms
from doctor.models import Appointment


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'


class SelectDateForm(forms.Form):
    date = forms.DateField(widget=DateInput)


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['doctor_profile', 'client']
        widgets = {
            'start': DateTimeInput(attrs={'readonly': 'readonly'}),
            'end': DateTimeInput(attrs={'readonly': 'readonly'}),
        }
