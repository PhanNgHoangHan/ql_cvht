from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from cvht.views import home_view

def home(request):
    return redirect('login')

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    
    path('', include('accounts.urls')),
    path('sinhvien/', include('sinhvien.urls')),
    path('covan/', include('covan.urls')),
    path('tuvantuvan/', include('tuvantuvan.urls')),
    path('dashboard/', home_view, name='dashboard'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
