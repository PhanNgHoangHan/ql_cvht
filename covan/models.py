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

    lop = models.OneToOneField(   # 🔥 mỗi lớp chỉ 1 cố vấn
        Lop,
        on_delete=models.CASCADE,
        related_name='covan'
    )

    class Meta:
        db_table = 'co_van'

    def __str__(self):
        return f"{self.ho_ten} - {self.lop}"
