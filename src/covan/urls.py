from django.urls import path
from . import views

app_name = 'covan'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sinhvien/', views.sinhvien_covan_list_view, name='sinhvien_list'),
    path('lich-tu-van/', views.lich_tu_van_covan_view, name='lich_tu_van'),
    path('thong-bao/', views.thong_bao_covan_view, name='thong_bao'),
    path('thong-ke/', views.thong_ke_covan_view, name='thong_ke'),
    path('phan-hoi/<int:phieu_id>/', views.phan_hoi_phieu_tu_van, name='phan_hoi'),
    path('bao-cao/', views.bao_cao_hoc_tap, name='bao_cao'),
]