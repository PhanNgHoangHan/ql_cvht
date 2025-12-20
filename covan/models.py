from django.db import models
from django.contrib.auth.models import User
from khoa.models import Khoa
from lop.models import Lop

class CoVan(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    ma_cv = models.CharField(max_length=10, unique=True)
    ho_ten = models.CharField(max_length=100)
    email = models.EmailField()
    dien_thoai = models.CharField(max_length=15)
    khoa = models.ForeignKey(
        Khoa,
        on_delete=models.CASCADE,
        related_name='ds_covan'
    )

    class Meta:
        db_table = 'co_van'

    def __str__(self):
        return self.ho_ten


class PhanCongCoVan(models.Model):
    covan = models.ForeignKey(CoVan, on_delete=models.CASCADE)
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    nam_hoc = models.CharField(max_length=9)
    hoc_ky = models.IntegerField()

    class Meta:
        db_table = 'phan_cong_cv'
        unique_together = ('covan', 'lop', 'nam_hoc', 'hoc_ky')

    def __str__(self):
        return f"{self.covan} - {self.lop}"
