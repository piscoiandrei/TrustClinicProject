from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include


def redirect_home(request):
    return redirect('visitor:home')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_home),
    path('visitor/', include('visitor.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


