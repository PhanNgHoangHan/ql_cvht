from django.contrib import admin
from .models import CoVan

@admin.register(CoVan)
class CoVanAdmin(admin.ModelAdmin):
    list_display = (
        'ma_cv',
        'ho_ten',
        'khoa',
        'lop',      # 👈 hiển thị lớp phụ trách
        'email',
        'dien_thoai'
    )
    list_filter = ('khoa', 'lop')
    search_fields = ('ma_cv', 'ho_ten', 'email')
