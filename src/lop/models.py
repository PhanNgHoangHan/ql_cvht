from django.db import models
from khoa.models import Khoa

class Lop(models.Model):
    ma_lop = models.CharField(max_length=10, primary_key=True)
    ten_lop = models.CharField(max_length=50)
    khoa = models.ForeignKey(
        Khoa,
        on_delete=models.CASCADE,
        related_name='ds_lop'
    )

    class Meta:
        db_table = 'lop'

    def __str__(self):
        return self.ten_lop
