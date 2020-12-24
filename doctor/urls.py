from django.urls import path
from .views import *

app_name = 'doctor'
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard')
]
