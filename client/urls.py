from django.urls import path
from .views import *

app_name = 'client'
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('specializations/', specializations, name='specializations'),
    path('specialization/detail/<str:pk>', specialization_detail,
         name='specialization_detail'),
    path('doctors/', doctors, name='doctors'),
    path('doctor/detail/<str:user_pk>/<str:profile_pk>/', doctor_detail,
         name='doctor_detail'),
    path('clinics/', clinics, name='clinics'),
    path('clinics/detail/<str:pk>/', clinic_detail, name='clinic_detail')
]
