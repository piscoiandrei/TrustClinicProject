from django.urls import path
from .views import *

app_name = 'chat'
urlpatterns = [
    path('operator/<str:pk>/', operator, name='operator'),
    path('client/<str:pk>/', client, name='client'),
    path('operator/,', operator_session, name='operator_session'),
    path('client/,', client_session, name='client_session'),
]
