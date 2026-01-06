#!/usr/bin/env python
"""
Script để xóa và tạo lại dữ liệu mẫu
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ql_cvht.settings')
django.setup()

from django.contrib.auth.models import User
from sinhvien.models import SinhVien
from covan.models import CoVan
from ketqua.models import KetQuaMonHoc, DiemHocTap, DiemRenLuyen
from tuvantuvan.models import PhieuTuVan, DanhGia, LichTuVan

def reset_data():
    print("=== XÓA DỮ LIỆU CŨ ===")
    
    # Xóa dữ liệu liên quan
    KetQuaMonHoc.objects.all().delete()
    DiemHocTap.objects.all().delete()
    DiemRenLuyen.objects.all().delete()
    DanhGia.objects.all().delete()
    PhieuTuVan.objects.all().delete()
    LichTuVan.objects.all().delete()
    
    # Xóa users (trừ admin)
    User.objects.filter(username__in=['sv001', 'sv002', 'sv003', 'covan01']).delete()
    
    print("✓ Đã xóa dữ liệu cũ")
    
    print("\n=== TẠO LẠI DỮ LIỆU MỚI ===")
    
    # Chạy lại setup
    import setup_system
    setup_system.create_sample_data()
    
    print("\n✓ Hoàn thành tạo lại dữ liệu")

if __name__ == '__main__':
    reset_data()