from django.contrib import admin
from .models import LichTuVan, PhieuTuVan, DanhGia

@admin.register(LichTuVan)
class LichTuVanAdmin(admin.ModelAdmin):
    list_display = ('covan', 'thoi_gian', 'dia_diem')
    list_filter = ('covan',)


@admin.register(PhieuTuVan)
class PhieuTuVanAdmin(admin.ModelAdmin):
    list_display = ('sinh_vien', 'covan', 'thoi_gian')
    list_filter = ('covan',)


@admin.register(DanhGia)
class DanhGiaAdmin(admin.ModelAdmin):
    list_display = ('phieu', 'diem_danh_gia')
    list_filter = ('diem_danh_gia',)
