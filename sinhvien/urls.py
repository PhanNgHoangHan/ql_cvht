from django.urls import path
from .views import dashboard
from .views import sinhvien_list_view

urlpatterns = [
    path('dashboard/', dashboard, name='sv_dashboard'),
]


urlpatterns = [
    path('', sinhvien_list_view, name='sinhvien'),
]