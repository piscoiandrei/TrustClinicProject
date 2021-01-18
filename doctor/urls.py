from django.urls import path
from .views import *

app_name = 'doctor'
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('appointment/delete/<str:pk>', appointment_delete,
         name='appointment_delete'),
    path('working-hours/<str:pk>/', hours_update,
         name='working_hours')

]
