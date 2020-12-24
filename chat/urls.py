from django.urls import path
from .views import *

urlpatterns = [
    path('operator/<str:pk>/', operator, name='operator'),
    path('client/<str:pk>/', client, name='client'),
]