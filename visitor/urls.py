from django.urls import path
from visitor import views as visitor_view

app_name = 'visitor'
urlpatterns = [
    path('', visitor_view.home, name='home'),
    path('login_redirect/', visitor_view.login_redirect, name='login_redirect')
]
