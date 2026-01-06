from django.db import models

class Khoa(models.Model):
    ma_khoa = models.CharField(max_length=10, primary_key=True)
    ten_khoa = models.CharField(max_length=100)
    dien_thoai = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = 'khoa'

    def __str__(self):
        return self.ten_khoa
