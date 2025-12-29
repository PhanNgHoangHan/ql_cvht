from django.contrib import admin
from .models import Lop

@admin.register(Lop)
class LopAdmin(admin.ModelAdmin):
    list_display = ('ma_lop', 'ten_lop', 'khoa')
    list_filter = ('khoa',)
    search_fields = ('ma_lop', 'ten_lop')
