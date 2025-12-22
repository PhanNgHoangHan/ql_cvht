from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from sinhvien.models import SinhVien
from covan.models import CoVan
from ketqua.models import DiemHocTap, DiemRenLuyen, KetQuaMonHoc

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
def sinhvien_detail_view(request, pk):
    sinhvien = get_object_or_404(SinhVien, pk=pk)

    diem_hoc_tap = DiemHocTap.objects.filter(sinh_vien=sinhvien)
    diem_ren_luyen = DiemRenLuyen.objects.filter(sinh_vien=sinhvien)

    context = {
        'sinhvien': sinhvien,
        'diem_hoc_tap': diem_hoc_tap,
        'diem_ren_luyen': diem_ren_luyen,
    }
    return render(request, 'sinhvien/detail.html', context)

@login_required
def ket_qua_hoc_tap_view(request, pk):
    sinhvien = get_object_or_404(SinhVien, pk=pk)

    mon_hoc = KetQuaMonHoc.objects.filter(sinh_vien=sinhvien)

    return render(request, 'sinhvien/kqhoctap.html', {
        'sinhvien': sinhvien,
        'mon_hoc': mon_hoc,
    })
