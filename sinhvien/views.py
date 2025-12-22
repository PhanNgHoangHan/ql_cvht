from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from sinhvien.models import SinhVien
from covan.models import CoVan
from ketqua.models import DiemHocTap, DiemRenLuyen, KetQuaMonHoc
from django.db.models import Avg
from django.db.models import Sum, F, FloatField
from ketqua.models import HocKy


def is_sinhvien(user):
    return user.groups.filter(name='SINH_VIEN').exists()

@login_required
@user_passes_test(is_sinhvien)
def dashboard(request):
    return render(request, 'sinhvien/dashboard.html')

@login_required(login_url='/login/')
def sinhvien_list_view(request):
    user = request.user
    sinhviens = []

    # 🔹 Nếu là CỐ VẤN
    if hasattr(user, 'covan'):
        lop = user.covan.lop
        sinhviens = SinhVien.objects.filter(lop=lop)

    # 🔹 Nếu là SINH VIÊN
    elif hasattr(user, 'sinhvien'):
        lop = user.sinhvien.lop
        sinhviens = SinhVien.objects.filter(lop=lop)

    context = {
        'sinhviens': sinhviens,
        'lop': lop if sinhviens else None
    }
    return render(request, 'sinhvien/list.html', context)


@login_required
def ket_qua_hoc_tap_view(request, pk):
    sinhvien = get_object_or_404(SinhVien, pk=pk)

    mon_hoc = KetQuaMonHoc.objects.filter(
        sinh_vien=sinhvien
    ).select_related('mon_hoc', 'hoc_ky')

    # 🔹 LẤY GIÁ TRỊ FILTER TỪ GET
    hoc_ky_id = request.GET.get('hoc_ky')
    ket_qua = request.GET.get('ket_qua')

    if hoc_ky_id:
        mon_hoc = mon_hoc.filter(hoc_ky_id=hoc_ky_id)

    if ket_qua:
        mon_hoc = mon_hoc.filter(ket_qua=ket_qua)

    # 🔹 DANH SÁCH HỌC KỲ ĐỂ ĐỔ VÀO SELECT
    hoc_kys = HocKy.objects.all()

    return render(request, 'sinhvien/kqhoctap.html', {
        'sinhvien': sinhvien,
        'mon_hoc': mon_hoc,
        'hoc_kys': hoc_kys,
        'selected_hoc_ky': hoc_ky_id,
        'selected_ket_qua': ket_qua,
    })




@login_required
def sinhvien_detail_view(request, pk):
    sinhvien = get_object_or_404(SinhVien, pk=pk)

    diem_hoc_tap = DiemHocTap.objects.filter(sinh_vien=sinhvien)
    diem_ren_luyen = DiemRenLuyen.objects.filter(sinh_vien=sinhvien)

    for d in diem_hoc_tap:
        qs = KetQuaMonHoc.objects.filter(
            sinh_vien=sinhvien,
            hoc_ky=d.hoc_ky
        )

        tong_diem = qs.aggregate(
            tong=Sum(
                F('diem_tong_ket') * F('mon_hoc__so_tin_chi'),
                output_field=FloatField()
            )
        )['tong'] or 0

        tong_tin_chi = qs.aggregate(
            tc=Sum('mon_hoc__so_tin_chi')
        )['tc'] or 0

        d.diem_trung_binh = round(
            tong_diem / tong_tin_chi, 2
        ) if tong_tin_chi > 0 else 0

        # Xếp loại
        if d.diem_trung_binh >= 3.6:
            d.xep_loai = 'Xuất sắc'
        elif d.diem_trung_binh >= 3.2:
            d.xep_loai = 'Giỏi'
        elif d.diem_trung_binh >= 2.5:
            d.xep_loai = 'Khá'
        elif d.diem_trung_binh >= 2:
            d.xep_loai = 'Trung bình'
        else:
            d.xep_loai = 'Yếu'

        d.save()

    return render(request, 'sinhvien/detail.html', {
        'sinhvien': sinhvien,
        'diem_hoc_tap': diem_hoc_tap,
        'diem_ren_luyen': diem_ren_luyen,
    })

        
