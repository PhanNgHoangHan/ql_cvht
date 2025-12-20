from django.contrib import admin
from .models import CoVan, PhanCongCoVan

@admin.register(CoVan)
class CoVanAdmin(admin.ModelAdmin):
    list_display = ('ma_cv', 'ho_ten', 'khoa', 'email')
    list_filter = ('khoa',)
    search_fields = ('ma_cv', 'ho_ten')


@admin.register(PhanCongCoVan)
class PhanCongCoVanAdmin(admin.ModelAdmin):
    list_display = ('covan', 'lop', 'nam_hoc', 'hoc_ky')
    list_filter = ('nam_hoc', 'hoc_ky')
