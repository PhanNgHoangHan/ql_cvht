from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from sinhvien.models import SinhVien
from covan.models import CoVan

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