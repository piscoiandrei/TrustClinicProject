from django.urls import path
from django.contrib.auth.views import LoginView
from .views import Login

app_name = 'accounts'

urlpatterns = [
    path('login/', Login.as_view(template_name='accounts/login.html'),
         name='login'),
]
