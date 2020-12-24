from django.urls import path
from .views import *

app_name = 'chat'
urlpatterns = [
    path('operator/<str:pk>/', operator, name='operator'),
    path('client/<str:pk>/', client, name='client'),
]