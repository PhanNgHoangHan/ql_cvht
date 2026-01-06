#!/usr/bin/env python
"""
Script khởi tạo dữ liệu mẫu cho Docker deployment
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ql_cvht.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.db import transaction

def create_groups():
    """Tạo các nhóm người dùng"""
    print("Tạo các nhóm người dùng...")
    
    sinh_vien_group, created = Group.objects.get_or_create(name='SINH_VIEN')
    if created:
        print("✅ Đã tạo nhóm SINH_VIEN")
    
    co_van_group, created = Group.objects.get_or_create(name='CO_VAN')
    if created:
        print("✅ Đã tạo nhóm CO_VAN")

def create_admin_user():
    """Tạo tài khoản admin"""
    print("Tạo tài khoản admin...")
    
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@tvu.edu.vn',
            password='admin123',
            first_name='Admin',
            last_name='System'
        )
        print("✅ Đã tạo tài khoản admin (admin/admin123)")
    else:
        print("ℹ️  Tài khoản admin đã tồn tại")

def main():
    """Hàm chính"""
    print("=== KHỞI TẠO DỮ LIỆU HỆ THỐNG CVHT TVU ===")
    
    try:
        with transaction.atomic():
            create_groups()
            create_admin_user()
            
        print("\n✅ Khởi tạo dữ liệu thành công!")
        print("\nThông tin đăng nhập:")
        print("- Admin: admin/admin123")
        print("- URL: http://localhost:8000/admin/")
        
    except Exception as e:
        print(f"\n❌ Lỗi khởi tạo dữ liệu: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()