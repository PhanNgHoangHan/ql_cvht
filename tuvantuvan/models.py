from django.db import models
from covan.models import CoVan
from sinhvien.models import SinhVien

class LichTuVan(models.Model):
    covan = models.ForeignKey(CoVan, on_delete=models.CASCADE)
    thoi_gian = models.DateTimeField()
    dia_diem = models.CharField(max_length=100)
    noi_dung_du_kien = models.TextField()

    class Meta:
        db_table = 'lich_tu_van'

    def __str__(self):
        return f"Lịch {self.covan} - {self.thoi_gian}"


class PhieuTuVan(models.Model):
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    covan = models.ForeignKey(CoVan, on_delete=models.CASCADE)
    thoi_gian = models.DateTimeField()
    noi_dung_tu_van = models.TextField()
    ket_qua = models.TextField()

    class Meta:
        db_table = 'phieu_tu_van'

    def __str__(self):
        return f"Phiếu {self.sinh_vien} - {self.covan}"


class DanhGia(models.Model):
    phieu = models.OneToOneField(
        PhieuTuVan,
        on_delete=models.CASCADE
    )
    diem_danh_gia = models.IntegerField()
    nhan_xet = models.TextField(blank=True)

    class Meta:
        db_table = 'danh_gia'

    def __str__(self):
        return f"Đánh giá {self.phieu}"
