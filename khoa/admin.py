from django.contrib import admin
from .models import Khoa

@admin.register(Khoa)
class KhoaAdmin(admin.ModelAdmin):
    list_display = ('ma_khoa', 'ten_khoa', 'dien_thoai', 'email')
    search_fields = ('ma_khoa', 'ten_khoa')
