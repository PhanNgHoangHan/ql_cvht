from django.urls import path
from .views import dashboard
from .views import sinhvien_list_view
from . import views


urlpatterns = [
    path('dashboard/', dashboard, name='sv_dashboard'),
]


urlpatterns = [
    path('', sinhvien_list_view, name='sinhvien'),
    path('<int:pk>/', views.sinhvien_detail_view, name='sinhvien_detail'),
    path('<int:pk>/ket-qua-hoc-tap/', views.ket_qua_hoc_tap_view, name='ket_qua_hoc_tap'),
]