from django.contrib import admin
from .models import LichTuVan, PhieuTuVan, DanhGia

class LichTuVanAdmin(admin.ModelAdmin):
    list_display = ('covan', 'thoi_gian', 'dia_diem')
    list_filter = ('covan',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Cố vấn chỉ xem lịch của mình
        if hasattr(request.user, 'covan'):
            return qs.filter(covan=request.user.covan)
            
        return qs
    
    def save_model(self, request, obj, form, change):
        # Tự động gán cố vấn hiện tại
        if hasattr(request.user, 'covan') and not change:
            obj.covan = request.user.covan
        super().save_model(request, obj, form, change)

class PhieuTuVanAdmin(admin.ModelAdmin):
    list_display = ('sinh_vien', 'covan', 'thoi_gian', 'ket_qua')
    list_filter = ('covan', 'ket_qua')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Cố vấn chỉ xem phiếu của mình
        if hasattr(request.user, 'covan'):
            return qs.filter(covan=request.user.covan)
        
        # Sinh viên chỉ xem phiếu của mình
        if hasattr(request.user, 'sinhvien'):
            return qs.filter(sinh_vien=request.user.sinhvien)
            
        return qs

class DanhGiaAdmin(admin.ModelAdmin):
    list_display = ('phieu', 'diem_danh_gia', 'nhan_xet')
    list_filter = ('diem_danh_gia',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Cố vấn chỉ xem đánh giá của sinh viên trong lớp
        if hasattr(request.user, 'covan'):
            return qs.filter(phieu__covan=request.user.covan)
        
        # Sinh viên chỉ xem đánh giá của mình
        if hasattr(request.user, 'sinhvien'):
            return qs.filter(phieu__sinh_vien=request.user.sinhvien)
            
        return qs

admin.site.register(LichTuVan, LichTuVanAdmin)
admin.site.register(PhieuTuVan, PhieuTuVanAdmin)
admin.site.register(DanhGia, DanhGiaAdmin)
