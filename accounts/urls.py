from django.urls import path, reverse_lazy
from .views import Login, EditProfile, Register
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

app_name = 'accounts'

urlpatterns = [
    path('login/', Login.as_view(template_name='accounts/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='accounts/logout.html'),
         name='logout'),
    path('edit-profile/<str:pk>/',
         EditProfile.as_view(success_url=reverse_lazy('client:dashboard')),
         name='edit_profile'),
    path('change-password/', PasswordChangeView.as_view(
        success_url=reverse_lazy('accounts:change_password_done'),
        template_name='accounts/change_password.html',
    ),
         name='change_password'),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='accounts/change_password_done.html',
    ),
         name='change_password_done'),

    path('register/', Register.as_view(), name='register'),

    # password reset urls

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             success_url=reverse_lazy('accounts:password_reset_done'),
             email_template_name='accounts/email/password_reset_email.html', ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete'), ),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]
