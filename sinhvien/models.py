from django.db import models
from django.contrib.auth.models import User
from lop.models import Lop

class SinhVien(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    ma_sv = models.CharField(max_length=10, unique=True)
    ho_ten = models.CharField(max_length=100)
    ngay_sinh = models.DateField(null=True, blank=True)
    gioi_tinh = models.CharField(max_length=10)
    email = models.EmailField()
    dien_thoai = models.CharField(max_length=15)
    lop = models.ForeignKey(
        Lop,
        on_delete=models.CASCADE,
        related_name='ds_sinh_vien'
    )

    class Meta:
        db_table = 'sinh_vien'

    def __str__(self):
        return self.ho_ten
