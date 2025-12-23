from django.urls import path
from . import views

app_name = 'sinhvien'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.sinhvien_list_view, name='list'),
    path('<int:pk>/', views.sinhvien_detail_view, name='detail'),
    path('<int:pk>/ket-qua-hoc-tap/', views.ket_qua_hoc_tap_view, name='ket_qua_hoc_tap'),
    path('<int:pk>/thong-ke/', views.thong_ke_sinhvien_view, name='thong_ke'),
    path('lich-tu-van/', views.lich_tu_van_sinhvien_view, name='lich_tu_van'),
]