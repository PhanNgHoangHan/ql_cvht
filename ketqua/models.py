from django.db import models
from sinhvien.models import SinhVien

class HocKy(models.Model):
    nam_hoc = models.CharField(max_length=20)
    hoc_ky = models.IntegerField()

    def __str__(self):
        return f"{self.nam_hoc} - HK{self.hoc_ky}"


class DiemHocTap(models.Model):
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    hoc_ky = models.ForeignKey(HocKy, on_delete=models.CASCADE)
    diem_trung_binh = models.FloatField()
    xep_loai = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.sinh_vien} - {self.hoc_ky}"


class DiemRenLuyen(models.Model):
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    hoc_ky = models.ForeignKey(HocKy, on_delete=models.CASCADE)
    diem_ren_luyen = models.IntegerField()
    xep_loai = models.CharField(max_length=50)
    ghi_chu = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.sinh_vien} - {self.hoc_ky}"

class MonHoc(models.Model):
    ma_mon = models.CharField(max_length=20, unique=True)
    ten_mon = models.CharField(max_length=100)
    so_tin_chi = models.IntegerField()

    def __str__(self):
        return self.ten_mon


class KetQuaMonHoc(models.Model):
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    mon_hoc = models.ForeignKey(MonHoc, on_delete=models.CASCADE)
    hoc_ky = models.ForeignKey(HocKy, on_delete=models.CASCADE)

    diem_qua_trinh = models.FloatField()
    diem_thi = models.FloatField()
    diem_tong_ket = models.FloatField()
    ket_qua = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.sinh_vien} - {self.mon_hoc}"
