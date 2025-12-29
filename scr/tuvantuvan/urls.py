from django.urls import path
from . import views

app_name = 'tuvantuvan'

urlpatterns = [
    path('dang-ky-lich/', views.dang_ky_lich_tu_van, name='dang_ky_lich'),
    path('lich-tu-van-sinhvien/', views.lich_tu_van_sinhvien, name='lich_tu_van_sinhvien'),
    path('danh-gia/<int:phieu_id>/', views.danh_gia_phieu_tu_van, name='danh_gia'),
    path('thong-bao-sinhvien/', views.thong_bao_sinhvien, name='thong_bao_sinhvien'),
    path('tao-lich/', views.tao_lich_tu_van, name='tao_lich'),
    path('huy-lich/<int:phieu_id>/', views.huy_lich_tu_van, name='huy_lich'),
]