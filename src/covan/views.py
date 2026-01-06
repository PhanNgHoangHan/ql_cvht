from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q, Sum, F, FloatField, Avg
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import json
from datetime import datetime

from covan.models import CoVan
from sinhvien.models import SinhVien
from ketqua.models import KetQuaMonHoc, HocKy, DiemHocTap, DiemRenLuyen
from tuvantuvan.models import PhieuTuVan, DanhGia, LichTuVan
from accounts.decorators import covan_required, is_covan

@covan_required
def dashboard(request):
    """Dashboard cho cố vấn"""
    covan = request.user.covan
    
    # Thống kê cơ bản
    tong_sinh_vien = SinhVien.objects.filter(lop=covan.lop).count()
    phieu_cho_phan_hoi = PhieuTuVan.objects.filter(
        covan=covan, 
        trang_thai='cho_phan_hoi'
    ).count()
    
    danh_gia_moi = DanhGia.objects.filter(
        phieu__covan=covan,
        phieu__trang_thai__in=['cho_phan_hoi', 'da_phan_hoi']  # Loại bỏ đánh giá từ phiếu đã hủy
    ).order_by('-id')[:5]
    
    context = {
        'covan': covan,
        'tong_sinh_vien': tong_sinh_vien,
        'phieu_cho_phan_hoi': phieu_cho_phan_hoi,
        'danh_gia_moi': danh_gia_moi,
    }
    return render(request, 'covan/dashboard.html', context)

@covan_required
def sinhvien_covan_list_view(request):
    """Danh sách sinh viên trong lớp cố vấn phụ trách"""
    covan = request.user.covan
    sinhviens = SinhVien.objects.filter(lop=covan.lop)
    
    context = {
        'sinhviens': sinhviens,
        'lop': covan.lop,
        'covan': covan
    }
    return render(request, 'covan/sinhvien_list.html', context)

@covan_required
def lich_tu_van_covan_view(request):
    """Lịch tư vấn của cố vấn - hiển thị phiếu tư vấn chờ phản hồi và lịch sử"""
    covan = request.user.covan
    
    # Phiếu tư vấn chờ phản hồi (chỉ cần kiểm tra trạng thái)
    phieu_cho_phan_hoi = PhieuTuVan.objects.filter(
        covan=covan,
        trang_thai='cho_phan_hoi'  # Chỉ lấy những phiếu chờ phản hồi
    ).select_related('sinh_vien', 'lich_tu_van').order_by('-thoi_gian')
    
    # Lịch sử phản hồi (đã phản hồi)
    lich_su_phan_hoi = PhieuTuVan.objects.filter(
        covan=covan,
        trang_thai='da_phan_hoi'
    ).select_related('sinh_vien', 'lich_tu_van').order_by('-thoi_gian')
    
    context = {
        'phieu_cho_phan_hoi': phieu_cho_phan_hoi,
        'lich_su_phan_hoi': lich_su_phan_hoi,
        'covan': covan
    }
    
    return render(request, 'covan/lich_tu_van.html', context)

@covan_required
def thong_bao_covan_view(request):
    """Thông báo cho cố vấn - lịch tư vấn và đánh giá từ sinh viên"""
    covan = request.user.covan
    
    # Lịch tư vấn mới từ sinh viên (chỉ những phiếu chưa bị hủy)
    lich_tu_van_moi = PhieuTuVan.objects.filter(
        covan=covan,
        trang_thai__in=['cho_phan_hoi', 'da_phan_hoi']  # Loại bỏ phiếu đã hủy
    ).select_related('sinh_vien').order_by('-thoi_gian')[:10]
    
    # Đánh giá từ sinh viên (chỉ từ phiếu chưa bị hủy)
    danh_gia_sinh_vien = DanhGia.objects.filter(
        phieu__covan=covan,
        phieu__trang_thai__in=['cho_phan_hoi', 'da_phan_hoi']  # Loại bỏ đánh giá từ phiếu đã hủy
    ).select_related('phieu__sinh_vien').order_by('-id')[:10]
    
    context = {
        'lich_tu_van_moi': lich_tu_van_moi,
        'danh_gia_sinh_vien': danh_gia_sinh_vien,
        'covan': covan
    }
    return render(request, 'covan/thong_bao.html', context)

@covan_required
def thong_ke_covan_view(request):
    """Thống kê cho cố vấn"""
    covan = request.user.covan
    
    # Lấy học kỳ được chọn
    hoc_ky_id = request.GET.get('hoc_ky', 'all')
    
    # Sinh viên trong lớp
    sinhviens = SinhVien.objects.filter(lop=covan.lop)
    
    # Query kết quả môn học
    ket_qua_query = KetQuaMonHoc.objects.filter(sinh_vien__lop=covan.lop)
    
    if hoc_ky_id != 'all':
        ket_qua_query = ket_qua_query.filter(hoc_ky_id=hoc_ky_id)
    
    # Debug: In ra kết quả để kiểm tra
    all_results = list(ket_qua_query.values('sinh_vien__ho_ten', 'mon_hoc__ten_mon', 'ket_qua', 'diem_tong_ket'))
    print(f"Debug - Tất cả kết quả lớp {covan.lop.ten_lop}: {all_results[:10]}")  # Chỉ in 10 kết quả đầu
    
    # Lấy tất cả giá trị ket_qua để debug
    unique_values = ket_qua_query.values_list('ket_qua', flat=True).distinct()
    print(f"Các giá trị ket_qua có trong DB: {list(unique_values)}")
    
    # Thống kê sinh viên có môn chưa đạt vs đạt toàn bộ môn
    # Tìm sinh viên có ít nhất 1 môn chưa đạt (sử dụng đúng giá trị "Chưa Đạt")
    sinh_vien_co_mon_chua_dat = sinhviens.filter(
        Q(id__in=ket_qua_query.filter(
            Q(ket_qua__iexact='Chưa Đạt') | Q(ket_qua__iexact='chua dat') | 
            Q(ket_qua__iexact='Chưa đạt') | Q(ket_qua__iexact='chua đạt')
        ).values_list('sinh_vien_id', flat=True))
    ).distinct()
    
    sinh_vien_chua_dat = sinh_vien_co_mon_chua_dat.count()
    sinh_vien_dat_tat_ca = sinhviens.count() - sinh_vien_chua_dat
    
    print(f"Debug - Thống kê lớp: Có môn chưa đạt={sinh_vien_chua_dat}, Đạt tất cả={sinh_vien_dat_tat_ca}")
    
    # Thống kê điểm đánh giá trung bình (chỉ từ phiếu chưa bị hủy)
    diem_danh_gia_tb = DanhGia.objects.filter(
        phieu__covan=covan,
        phieu__trang_thai__in=['cho_phan_hoi', 'da_phan_hoi']  # Loại bỏ đánh giá từ phiếu đã hủy
    ).aggregate(tb=Avg('diem_danh_gia'))['tb'] or 0
    
    # Danh sách học kỳ
    hoc_kys = HocKy.objects.all()
    
    # Dữ liệu biểu đồ
    chart_data = {
        'labels': ['Có môn chưa đạt', 'Đạt toàn bộ môn'],
        'data': [sinh_vien_chua_dat, sinh_vien_dat_tat_ca],
        'backgroundColor': ['#dc3545', '#28a745']
    }
    
    context = {
        'covan': covan,
        'sinh_vien_chua_dat': sinh_vien_chua_dat,
        'sinh_vien_dat_tat_ca': sinh_vien_dat_tat_ca,
        'diem_danh_gia_tb': round(diem_danh_gia_tb, 2),
        'hoc_kys': hoc_kys,
        'selected_hoc_ky': hoc_ky_id,
        'chart_data': json.dumps(chart_data),
        'debug_results': all_results[:5],  # Thêm để debug
        'unique_ket_qua': list(unique_values)  # Debug giá trị
    }
    
    return render(request, 'covan/thong_ke.html', context)

@covan_required
def phan_hoi_phieu_tu_van(request, phieu_id):
    """Phản hồi phiếu tư vấn"""
    phieu = get_object_or_404(PhieuTuVan, id=phieu_id, covan=request.user.covan)
    
    if request.method == 'POST':
        ket_qua = request.POST.get('ket_qua')
        if ket_qua:
            phieu.ket_qua = ket_qua
            phieu.trang_thai = 'da_phan_hoi'  # Cập nhật trạng thái khi phản hồi
            phieu.save()
            return redirect('covan:lich_tu_van')
    
    return render(request, 'covan/phan_hoi_phieu.html', {'phieu': phieu})

@covan_required
def bao_cao_hoc_tap(request):
    """Xuất báo cáo học tập theo học kỳ/năm học"""
    covan = request.user.covan
    
    hoc_ky_id = request.GET.get('hoc_ky')
    nam_hoc = request.GET.get('nam_hoc')
    
    # Query sinh viên trong lớp
    sinhviens = SinhVien.objects.filter(lop=covan.lop)
    
    # Lấy điểm học tập và rèn luyện
    diem_query = DiemHocTap.objects.filter(sinh_vien__lop=covan.lop)
    ren_luyen_query = DiemRenLuyen.objects.filter(sinh_vien__lop=covan.lop)
    
    if hoc_ky_id:
        diem_query = diem_query.filter(hoc_ky_id=hoc_ky_id)
        ren_luyen_query = ren_luyen_query.filter(hoc_ky_id=hoc_ky_id)
    elif nam_hoc:
        diem_query = diem_query.filter(hoc_ky__nam_hoc=nam_hoc)
        ren_luyen_query = ren_luyen_query.filter(hoc_ky__nam_hoc=nam_hoc)
    
    # Tạo danh sách kết quả
    ket_qua = []
    tong_diem_rl = 0
    count_rl_cao = 0
    
    for sv in sinhviens:
        diem_ht = diem_query.filter(sinh_vien=sv).first()
        diem_rl = ren_luyen_query.filter(sinh_vien=sv).first()
        
        diem_hoc_tap = diem_ht.diem_trung_binh if diem_ht else 0
        diem_ren_luyen = diem_rl.diem_ren_luyen if diem_rl else 0
        
        # Tính thống kê
        tong_diem_rl += diem_ren_luyen
        if diem_ren_luyen >= 80:
            count_rl_cao += 1
        
        ket_qua.append({
            'sinh_vien': sv,
            'diem_hoc_tap': diem_hoc_tap,
            'xep_loai_ht': diem_ht.xep_loai if diem_ht else 'Chưa có',
            'diem_ren_luyen': diem_ren_luyen,
            'xep_loai_rl': diem_rl.xep_loai if diem_rl else 'Chưa có'
        })
    
    # Tính điểm trung bình rèn luyện
    diem_rl_tb = round(tong_diem_rl / len(ket_qua), 1) if ket_qua else 0
    
    # Danh sách học kỳ và năm học
    hoc_kys = HocKy.objects.all()
    nam_hocs = HocKy.objects.values_list('nam_hoc', flat=True).distinct()
    
    context = {
        'covan': covan,
        'ket_qua': ket_qua,
        'hoc_kys': hoc_kys,
        'nam_hocs': nam_hocs,
        'selected_hoc_ky': hoc_ky_id,
        'selected_nam_hoc': nam_hoc,
        'count_rl_cao': count_rl_cao,
        'diem_rl_tb': diem_rl_tb
    }
    
    return render(request, 'covan/bao_cao.html', context)
