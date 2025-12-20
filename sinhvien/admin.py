from django.contrib import admin
from .models import SinhVien

@admin.register(SinhVien)
class SinhVienAdmin(admin.ModelAdmin):
    list_display = ('ma_sv', 'ho_ten', 'lop', 'email')
    list_filter = ('lop',)
    search_fields = ('ma_sv', 'ho_ten', 'email')
