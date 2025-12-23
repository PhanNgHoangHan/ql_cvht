from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from sinhvien.models import SinhVien
from covan.models import CoVan
from tuvantuvan.models import PhieuTuVan, DanhGia, LichTuVan
from ketqua.models import KetQuaMonHoc, DiemHocTap, DiemRenLuyen

class Command(BaseCommand):
    help = 'Tạo các nhóm quyền SINH_VIEN và CO_VAN'

    def handle(self, *args, **options):
        # Tạo nhóm SINH_VIEN
        sinh_vien_group, created = Group.objects.get_or_create(name='SINH_VIEN')
        if created:
            self.stdout.write(self.style.SUCCESS('Đã tạo nhóm SINH_VIEN'))
        
        # Tạo nhóm CO_VAN
        co_van_group, created = Group.objects.get_or_create(name='CO_VAN')
        if created:
            self.stdout.write(self.style.SUCCESS('Đã tạo nhóm CO_VAN'))

        # Quyền cho SINH_VIEN
        sinh_vien_permissions = [
            # Xem thông tin cá nhân
            'view_sinhvien',
            # Xem kết quả học tập của mình
            'view_ketquamonhoc',
            'view_diemhoctap', 
            'view_diemrenluyen',
            # Tạo và xem phiếu tư vấn của mình
            'add_phieutuvan',
            'view_phieutuvan',
            # Tạo đánh giá
            'add_danhgia',
            'view_danhgia',
        ]

        # Quyền cho CO_VAN
        co_van_permissions = [
            # Xem thông tin sinh viên trong lớp
            'view_sinhvien',
            # Xem kết quả học tập sinh viên
            'view_ketquamonhoc',
            'view_diemhoctap',
            'view_diemrenluyen', 
            # Quản lý lịch tư vấn
            'add_lichtuvan',
            'change_lichtuvan',
            'view_lichtuvan',
            # Xem và phản hồi phiếu tư vấn
            'view_phieutuvan',
            'change_phieutuvan',
            # Xem đánh giá
            'view_danhgia',
        ]

        # Gán quyền cho nhóm SINH_VIEN
        for perm_codename in sinh_vien_permissions:
            try:
                permission = Permission.objects.get(codename=perm_codename)
                sinh_vien_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Không tìm thấy quyền: {perm_codename}')
                )

        # Gán quyền cho nhóm CO_VAN  
        for perm_codename in co_van_permissions:
            try:
                permission = Permission.objects.get(codename=perm_codename)
                co_van_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Không tìm thấy quyền: {perm_codename}')
                )

        self.stdout.write(
            self.style.SUCCESS('Đã thiết lập quyền cho các nhóm thành công!')
        )