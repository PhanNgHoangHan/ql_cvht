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
    TRANG_THAI_CHOICES = [
        ('cho_phan_hoi', 'Chờ phản hồi'),
        ('da_phan_hoi', 'Đã phản hồi'),
        ('da_huy', 'Đã hủy'),
    ]
    
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    covan = models.ForeignKey(CoVan, on_delete=models.CASCADE)

    lich_tu_van = models.ForeignKey(
        LichTuVan,
        on_delete=models.CASCADE,
        related_name='phieu_tu_van'
    )

    thoi_gian = models.DateTimeField()
    noi_dung_tu_van = models.TextField()
    ket_qua = models.TextField(blank=True)
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='cho_phan_hoi')

    class Meta:
        db_table = 'phieu_tu_van'


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
