from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect, resolve_url
from django.urls import path, include, reverse_lazy


def _redirect(request):
    user = request.user
    if user.is_authenticated:
        if user.is_operator:
            return redirect(
                reverse_lazy('chat:operator_session'))
        if user.is_doctor:
            return redirect(
                reverse_lazy('doctor:dashboard'))
        if user.is_staff or user.is_superuser:
            return redirect(resolve_url('/admin/'))
        if user.is_client:
            return redirect(
                reverse_lazy('client:dashboard'))
    else:
        return redirect('visitor:home')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', _redirect, name="_redirect"),
    path('visitor/', include('visitor.urls')),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('doctor/', include('doctor.urls')),
    path('client/', include('client.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
