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
    path('clinics/detail/<str:pk>/', clinic_detail, name='clinic_detail'),
    path('schedule/<str:doctor_pk>/', schedule, name='schedule'),
    path('appointments/<str:client_pk>/', appointments, name='appointments'),
    path('appointment/success/', appointment_success,
         name='appointment_success'),
    path('appointment/delete/confirm/<str:pk>', appointment_delete_confirm,
         name='appointment_delete_confirm'),
    path('appointment/delete/<str:pk>', appointment_delete,
         name='appointment_delete'),
    path('appointment/delete/done/', appointment_delete_done,
         name='appointment_delete_done')
]
