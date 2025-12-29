from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Sum, F, FloatField, Count, Q
from django.http import JsonResponse
import json

from sinhvien.models import SinhVien
from covan.models import CoVan
from ketqua.models import DiemHocTap, DiemRenLuyen, KetQuaMonHoc, HocKy, MonHoc
from tuvantuvan.models import PhieuTuVan, DanhGia, LichTuVan
from accounts.decorators import (
    sinhvien_required, 
    covan_required, 
    sinhvien_or_covan_required,
    check_sinhvien_access,
    is_sinhvien,
    is_covan
)

@sinhvien_required
def dashboard(request):
    """Dashboard cho sinh viên"""
    sinhvien = request.user.sinhvien
    
    # Thống kê cơ bản
    tong_phieu_tu_van = PhieuTuVan.objects.filter(sinh_vien=sinhvien).count()
    phieu_chua_danh_gia = PhieuTuVan.objects.filter(
        sinh_vien=sinhvien
    ).exclude(
        id__in=DanhGia.objects.values_list('phieu_id', flat=True)
    ).count()
    
    context = {
        'sinhvien': sinhvien,
        'tong_phieu_tu_van': tong_phieu_tu_van,
        'phieu_chua_danh_gia': phieu_chua_danh_gia,
    }
    return render(request, 'sinhvien/dashboard.html', context)

@sinhvien_or_covan_required
def sinhvien_list_view(request):
    """
    Danh sách sinh viên:
    - Sinh viên: chỉ xem thông tin của chính mình
    - Cố vấn: xem tất cả sinh viên trong lớp phụ trách
    """
    user = request.user
    sinhviens = []
    lop = None

    if is_covan(user) and hasattr(user, 'covan'):
        # Cố vấn xem tất cả sinh viên trong lớp
        lop = user.covan.lop
        sinhviens = SinhVien.objects.filter(lop=lop)
    elif is_sinhvien(user) and hasattr(user, 'sinhvien'):
        # Sinh viên chỉ xem thông tin của chính mình
        sinhviens = [user.sinhvien]
        lop = user.sinhvien.lop

    context = {
        'sinhviens': sinhviens,
        'lop': lop,
        'is_covan': is_covan(user),
        'is_sinhvien': is_sinhvien(user)
    }
    return render(request, 'sinhvien/list.html', context)


@check_sinhvien_access
def ket_qua_hoc_tap_view(request, pk):
    """Kết quả học tập với kiểm tra quyền truy cập"""
    sinhvien = get_object_or_404(SinhVien, pk=pk)

    mon_hoc = KetQuaMonHoc.objects.filter(
        sinh_vien=sinhvien
    ).select_related('mon_hoc', 'hoc_ky')

    # Lấy giá trị filter từ GET
    hoc_ky_id = request.GET.get('hoc_ky')
    ket_qua = request.GET.get('ket_qua')

    if hoc_ky_id:
        mon_hoc = mon_hoc.filter(hoc_ky_id=hoc_ky_id)

    if ket_qua:
        mon_hoc = mon_hoc.filter(ket_qua=ket_qua)

    # Danh sách học kỳ để đổ vào select
    hoc_kys = HocKy.objects.all()

    return render(request, 'sinhvien/kqhoctap.html', {
        'sinhvien': sinhvien,
        'mon_hoc': mon_hoc,
        'hoc_kys': hoc_kys,
        'selected_hoc_ky': hoc_ky_id,
        'selected_ket_qua': ket_qua,
        'is_covan': is_covan(request.user),
        'is_sinhvien': is_sinhvien(request.user)
    })




@check_sinhvien_access
def sinhvien_detail_view(request, pk):
    """Chi tiết sinh viên với kiểm tra quyền truy cập"""
    sinhvien = get_object_or_404(SinhVien, pk=pk)

    diem_hoc_tap = DiemHocTap.objects.filter(sinh_vien=sinhvien)
    diem_ren_luyen = DiemRenLuyen.objects.filter(sinh_vien=sinhvien)

    # Tính toán điểm trung bình cho từng học kỳ
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

    context = {
        'sinhvien': sinhvien,
        'diem_hoc_tap': diem_hoc_tap,
        'diem_ren_luyen': diem_ren_luyen,
        'is_covan': is_covan(request.user),
        'is_sinhvien': is_sinhvien(request.user)
    }
    return render(request, 'sinhvien/detail.html', context)

        
@sinhvien_required
def lich_tu_van_sinhvien_view(request):
    """Lịch tư vấn của sinh viên"""
    sinhvien = request.user.sinhvien

    # Lịch tư vấn = Phiếu tư vấn
    phieu_tu_van = PhieuTuVan.objects.filter(
        sinh_vien=sinhvien
    ).select_related('covan', 'lich_tu_van').order_by('-thoi_gian')

    # Đánh giá
    danh_gia = DanhGia.objects.filter(
        phieu__sinh_vien=sinhvien
    ).select_related('phieu')

    return render(request, 'sinhvien/lich_tu_van.html', {
        'lich_tu_van': phieu_tu_van,
        'danh_gia': danh_gia,
        'sinhvien': sinhvien
    })

@check_sinhvien_access  
def thong_ke_sinhvien_view(request, pk):
    """Thống kê điểm số cho sinh viên"""
    sinhvien = get_object_or_404(SinhVien, pk=pk)
    
    # Lấy học kỳ được chọn
    hoc_ky_id = request.GET.get('hoc_ky', 'all')
    
    # Query kết quả môn học
    ket_qua_query = KetQuaMonHoc.objects.filter(sinh_vien=sinhvien)
    
    if hoc_ky_id != 'all':
        ket_qua_query = ket_qua_query.filter(hoc_ky_id=hoc_ky_id)
    
    # Debug: In ra tất cả kết quả để kiểm tra
    all_results = list(ket_qua_query.values('mon_hoc__ten_mon', 'ket_qua', 'diem_tong_ket'))
    print(f"Debug - Tất cả kết quả của {sinhvien.ho_ten}: {all_results}")
    
    # Thống kê đạt/chưa đạt - sử dụng đúng giá trị "Đạt" và "Chưa Đạt"
    dat_count = ket_qua_query.filter(
        Q(ket_qua__iexact='Đạt') | Q(ket_qua__iexact='dat')
    ).count()
    
    chua_dat_count = ket_qua_query.filter(
        Q(ket_qua__iexact='Chưa Đạt') | Q(ket_qua__iexact='chua dat') | 
        Q(ket_qua__iexact='Chưa đạt') | Q(ket_qua__iexact='chua đạt')
    ).count()
    
    # Kiểm tra nếu tổng không khớp với số môn, có thể có giá trị khác
    total_subjects = ket_qua_query.count()
    calculated_total = dat_count + chua_dat_count
    
    if calculated_total != total_subjects and total_subjects > 0:
        print(f"Warning: Tổng không khớp. Tổng môn: {total_subjects}, Đã tính: {calculated_total}")
        # Lấy tất cả giá trị ket_qua để debug
        unique_values = ket_qua_query.values_list('ket_qua', flat=True).distinct()
        print(f"Các giá trị ket_qua có trong DB: {list(unique_values)}")
        
        # Nếu có giá trị khác, thử phân loại lại
        for result in ket_qua_query:
            if result.ket_qua not in ['Đạt', 'Chưa Đạt']:
                print(f"Giá trị lạ: '{result.ket_qua}' cho môn {result.mon_hoc.ten_mon}")
    
    thong_ke = {
        'dat': dat_count,
        'chua_dat': chua_dat_count
    }
    
    print(f"Debug - Thống kê: Đạt={dat_count}, Chưa đạt={chua_dat_count}")
    
    # Danh sách học kỳ
    hoc_kys = HocKy.objects.all()
    
    # Chuẩn bị dữ liệu cho biểu đồ
    chart_data = {
        'labels': ['Đạt', 'Chưa đạt'],
        'data': [thong_ke['dat'], thong_ke['chua_dat']],
        'backgroundColor': ['#28a745', '#dc3545']
    }
    
    context = {
        'sinhvien': sinhvien,
        'thong_ke': thong_ke,
        'hoc_kys': hoc_kys,
        'selected_hoc_ky': hoc_ky_id,
        'chart_data': json.dumps(chart_data),
        'is_covan': is_covan(request.user),
        'is_sinhvien': is_sinhvien(request.user),
        'debug_results': all_results  # Thêm để debug
    }
    
    return render(request, 'sinhvien/thong_ke.html', context)