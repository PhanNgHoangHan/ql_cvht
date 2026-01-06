from django.contrib import admin
from django.contrib.auth.models import User
from .models import SinhVien

class SinhVienAdmin(admin.ModelAdmin):
    list_display = ('ma_sv', 'ho_ten', 'lop', 'email')
    list_filter = ('lop',)
    search_fields = ('ma_sv', 'ho_ten', 'email')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Nếu là cố vấn, chỉ hiển thị sinh viên trong lớp phụ trách
        if hasattr(request.user, 'covan'):
            return qs.filter(lop=request.user.covan.lop)
        
        # Nếu là sinh viên, chỉ hiển thị chính mình
        if hasattr(request.user, 'sinhvien'):
            return qs.filter(id=request.user.sinhvien.id)
            
        return qs
    
    def has_change_permission(self, request, obj=None):
        # Sinh viên không được sửa thông tin
        if hasattr(request.user, 'sinhvien'):
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        # Sinh viên không được xóa
        if hasattr(request.user, 'sinhvien'):
            return False
        return super().has_delete_permission(request, obj)

admin.site.register(SinhVien, SinhVienAdmin)
