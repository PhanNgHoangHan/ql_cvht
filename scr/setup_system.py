#!/usr/bin/env python
"""
Script để thiết lập hệ thống quản lý CVHT
Chạy script này sau khi migrate database
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ql_cvht.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from khoa.models import Khoa
from lop.models import Lop
from sinhvien.models import SinhVien
from covan.models import CoVan
from ketqua.models import HocKy, MonHoc, KetQuaMonHoc, DiemHocTap, DiemRenLuyen

def create_groups():
    """Tạo các nhóm quyền"""
    print("Tạo các nhóm quyền...")
    
    sinh_vien_group, created = Group.objects.get_or_create(name='SINH_VIEN')
    if created:
        print("✓ Đã tạo nhóm SINH_VIEN")
    
    co_van_group, created = Group.objects.get_or_create(name='CO_VAN')
    if created:
        print("✓ Đã tạo nhóm CO_VAN")

def create_sample_data():
    """Tạo dữ liệu mẫu"""
    print("Tạo dữ liệu mẫu...")
    
    # Tạo khoa
    khoa, created = Khoa.objects.get_or_create(
        ma_khoa='CNTT',
        defaults={
            'ten_khoa': 'Công nghệ thông tin',
            'email': 'cntt@university.edu.vn',
            'dien_thoai': '0123456789'
        }
    )
    if created:
        print("✓ Đã tạo khoa CNTT")
    
    # Tạo lớp
    lop, created = Lop.objects.get_or_create(
        ma_lop='CNTT01',
        defaults={
            'ten_lop': 'Công nghệ thông tin 01',
            'khoa': khoa
        }
    )
    if created:
        print("✓ Đã tạo lớp CNTT01")
    
    # Tạo học kỳ
    hoc_ky1, created = HocKy.objects.get_or_create(
        nam_hoc='2023-2024',
        hoc_ky=1
    )
    if created:
        print("✓ Đã tạo học kỳ 2023-2024 HK1")
    
    hoc_ky2, created = HocKy.objects.get_or_create(
        nam_hoc='2023-2024',
        hoc_ky=2
    )
    if created:
        print("✓ Đã tạo học kỳ 2023-2024 HK2")
    
    # Tạo môn học
    mon_hoc_list = [
        ('MATH101', 'Toán cao cấp', 3),
        ('PROG101', 'Lập trình cơ bản', 4),
        ('ENG101', 'Tiếng Anh', 2),
        ('PHYS101', 'Vật lý đại cương', 3),
    ]
    
    for ma_mon, ten_mon, so_tin_chi in mon_hoc_list:
        mon_hoc, created = MonHoc.objects.get_or_create(
            ma_mon=ma_mon,
            defaults={
                'ten_mon': ten_mon,
                'so_tin_chi': so_tin_chi
            }
        )
        if created:
            print(f"✓ Đã tạo môn học {ten_mon}")
    
    # Tạo user cố vấn
    if not User.objects.filter(username='covan01').exists():
        user_covan = User.objects.create(
            username='covan01',
            password=make_password('123456'),
            first_name='Nguyễn',
            last_name='Văn Cố Vấn',
            email='covan01@university.edu.vn'
        )
        user_covan.groups.add(Group.objects.get(name='CO_VAN'))
        
        # Tạo profile cố vấn
        covan = CoVan.objects.create(
            user=user_covan,
            ma_cv='CV001',
            ho_ten='Nguyễn Văn Cố Vấn',
            email='covan01@university.edu.vn',
            dien_thoai='0987654321',
            khoa=khoa,
            lop=lop
        )
        print("✓ Đã tạo cố vấn: covan01/123456")
    
    # Tạo user sinh viên
    sinh_vien_data = [
        ('sv001', 'SV001', 'Nguyễn Văn A'),
        ('sv002', 'SV002', 'Trần Thị B'),
        ('sv003', 'SV003', 'Lê Văn C'),
    ]
    
    for username, ma_sv, ho_ten in sinh_vien_data:
        if not User.objects.filter(username=username).exists():
            user_sv = User.objects.create(
                username=username,
                password=make_password('123456'),
                first_name=ho_ten.split()[-1],
                last_name=' '.join(ho_ten.split()[:-1]),
                email=f'{username}@student.edu.vn'
            )
            user_sv.groups.add(Group.objects.get(name='SINH_VIEN'))
            
            # Tạo profile sinh viên
            sinh_vien = SinhVien.objects.create(
                user=user_sv,
                ma_sv=ma_sv,
                ho_ten=ho_ten,
                gioi_tinh='Nam' if 'Văn' in ho_ten else 'Nữ',
                email=f'{username}@student.edu.vn',
                dien_thoai='0123456789',
                lop=lop
            )
            
            # Tạo điểm học tập
            DiemHocTap.objects.create(
                sinh_vien=sinh_vien,
                hoc_ky=hoc_ky1,
                diem_trung_binh=3.2,
                xep_loai='Giỏi'
            )
            
            # Tạo điểm rèn luyện
            DiemRenLuyen.objects.create(
                sinh_vien=sinh_vien,
                hoc_ky=hoc_ky1,
                diem_ren_luyen=85,
                xep_loai='Tốt'
            )
            
            # Tạo kết quả môn học mẫu
            mon_hoc_objects = MonHoc.objects.all()
            for i, mon_hoc in enumerate(mon_hoc_objects):
                # Tạo điểm khác nhau cho mỗi sinh viên
                if username == 'sv001':
                    diem_qua_trinh = 8.5 if i < 3 else 4.0
                    diem_thi = 7.0 if i < 3 else 3.5
                    diem_tong_ket = 7.5 if i < 3 else 3.8
                    ket_qua = 'Đạt' if i < 3 else 'Chưa Đạt'
                elif username == 'sv002':
                    diem_qua_trinh = 9.0 if i < 2 else 5.0
                    diem_thi = 8.0 if i < 2 else 4.0
                    diem_tong_ket = 8.5 if i < 2 else 4.5
                    ket_qua = 'Đạt' if i < 2 else 'Chưa Đạt'
                else:  # sv003
                    diem_qua_trinh = 7.0
                    diem_thi = 6.5
                    diem_tong_ket = 6.8
                    ket_qua = 'Đạt'
                
                KetQuaMonHoc.objects.create(
                    sinh_vien=sinh_vien,
                    mon_hoc=mon_hoc,
                    hoc_ky=hoc_ky1,
                    diem_qua_trinh=diem_qua_trinh,
                    diem_thi=diem_thi,
                    diem_tong_ket=diem_tong_ket,
                    ket_qua=ket_qua
                )
            
            print(f"✓ Đã tạo sinh viên: {username}/123456")

def create_admin():
    """Tạo tài khoản admin"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@university.edu.vn',
            password='admin123'
        )
        print("✓ Đã tạo tài khoản admin: admin/admin123")

def main():
    print("=== THIẾT LẬP HỆ THỐNG QUẢN LÝ CVHT ===")
    
    try:
        create_groups()
        create_sample_data()
        create_admin()
        
        print("\n=== HOÀN THÀNH THIẾT LẬP ===")
        print("Tài khoản đã tạo:")
        print("- Admin: admin/admin123")
        print("- Cố vấn: covan01/123456")
        print("- Sinh viên: sv001/123456, sv002/123456, sv003/123456")
        print("\nTruy cập: http://localhost:8000/login/")
        
    except Exception as e:
        print(f"Lỗi: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()