#!/usr/bin/env python
"""
Script để kiểm tra dữ liệu trong database
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ql_cvht.settings')
django.setup()

from sinhvien.models import SinhVien
from ketqua.models import KetQuaMonHoc

def check_data():
    print("=== KIỂM TRA DỮ LIỆU ===")
    
    # Kiểm tra sinh viên
    sinhviens = SinhVien.objects.all()
    print(f"Số sinh viên: {sinhviens.count()}")
    
    for sv in sinhviens:
        print(f"\n--- Sinh viên: {sv.ho_ten} ({sv.ma_sv}) ---")
        
        # Kiểm tra kết quả môn học
        ket_qua = KetQuaMonHoc.objects.filter(sinh_vien=sv)
        print(f"Số môn học: {ket_qua.count()}")
        
        for kq in ket_qua:
            print(f"  {kq.mon_hoc.ten_mon}: {kq.diem_tong_ket} - {kq.ket_qua}")
        
        # Thống kê
        dat = ket_qua.filter(ket_qua='Đạt').count()
        chua_dat = ket_qua.filter(ket_qua='Chưa Đạt').count()
        dat_diem = ket_qua.filter(diem_tong_ket__gte=5.0).count()
        chua_dat_diem = ket_qua.filter(diem_tong_ket__lt=5.0).count()
        
        print(f"  Thống kê theo ket_qua: Đạt={dat}, Chưa Đạt={chua_dat}")
        print(f"  Thống kê theo điểm: Đạt(>=5)={dat_diem}, Chưa đạt(<5)={chua_dat_diem}")
        
        # Kiểm tra các giá trị ket_qua có trong DB
        unique_ket_qua = ket_qua.values_list('ket_qua', flat=True).distinct()
        print(f"  Các giá trị ket_qua: {list(unique_ket_qua)}")

if __name__ == '__main__':
    check_data()