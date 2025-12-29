#!/usr/bin/env python
"""
Script để test chức năng báo cáo
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ql_cvht.settings')
django.setup()

from django.contrib.auth.models import User
from covan.models import CoVan
from sinhvien.models import SinhVien
from ketqua.models import DiemHocTap, DiemRenLuyen, HocKy

def test_report_data():
    print("=== KIỂM TRA DỮ LIỆU BÁO CÁO ===")
    
    # Kiểm tra cố vấn
    try:
        user_covan = User.objects.get(username='covan01')
        covan = user_covan.covan
        print(f"✓ Cố vấn: {covan.ho_ten} - Lớp: {covan.lop.ten_lop}")
        
        # Kiểm tra sinh viên trong lớp
        sinhviens = SinhVien.objects.filter(lop=covan.lop)
        print(f"✓ Số sinh viên trong lớp: {sinhviens.count()}")
        
        # Kiểm tra điểm học tập
        diem_hoc_tap = DiemHocTap.objects.filter(sinh_vien__lop=covan.lop)
        print(f"✓ Số bản ghi điểm học tập: {diem_hoc_tap.count()}")
        
        # Kiểm tra điểm rèn luyện
        diem_ren_luyen = DiemRenLuyen.objects.filter(sinh_vien__lop=covan.lop)
        print(f"✓ Số bản ghi điểm rèn luyện: {diem_ren_luyen.count()}")
        
        # Kiểm tra học kỳ
        hoc_kys = HocKy.objects.all()
        print(f"✓ Số học kỳ: {hoc_kys.count()}")
        for hk in hoc_kys:
            print(f"  - {hk.nam_hoc} HK{hk.hoc_ky}")
        
        # Test tạo báo cáo
        print("\n=== TEST TẠO BÁO CÁO ===")
        ket_qua = []
        tong_diem_rl = 0
        count_rl_cao = 0
        
        for sv in sinhviens:
            diem_ht = diem_hoc_tap.filter(sinh_vien=sv).first()
            diem_rl = diem_ren_luyen.filter(sinh_vien=sv).first()
            
            diem_hoc_tap_val = diem_ht.diem_trung_binh if diem_ht else 0
            diem_ren_luyen_val = diem_rl.diem_ren_luyen if diem_rl else 0
            
            tong_diem_rl += diem_ren_luyen_val
            if diem_ren_luyen_val >= 80:
                count_rl_cao += 1
            
            ket_qua.append({
                'sinh_vien': sv.ho_ten,
                'ma_sv': sv.ma_sv,
                'diem_hoc_tap': diem_hoc_tap_val,
                'xep_loai_ht': diem_ht.xep_loai if diem_ht else 'Chưa có',
                'diem_ren_luyen': diem_ren_luyen_val,
                'xep_loai_rl': diem_rl.xep_loai if diem_rl else 'Chưa có'
            })
            
            print(f"  {sv.ma_sv} - {sv.ho_ten}: HT={diem_hoc_tap_val}, RL={diem_ren_luyen_val}")
        
        diem_rl_tb = round(tong_diem_rl / len(ket_qua), 1) if ket_qua else 0
        
        print(f"\n✓ Tổng sinh viên: {len(ket_qua)}")
        print(f"✓ Sinh viên có điểm RL ≥ 80: {count_rl_cao}")
        print(f"✓ Điểm RL trung bình: {diem_rl_tb}")
        
        print("\n✅ Dữ liệu báo cáo OK!")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_report_data()