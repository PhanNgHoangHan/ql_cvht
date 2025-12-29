from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from tuvantuvan.models import LichTuVan, PhieuTuVan, DanhGia
from covan.models import CoVan
from accounts.decorators import sinhvien_required, covan_required, sinhvien_or_covan_required, is_sinhvien, is_covan

@sinhvien_required
def dang_ky_lich_tu_van(request):
    """Sinh viên đăng ký lịch tư vấn"""
    sinhvien = request.user.sinhvien
    covan = sinhvien.lop.covan
    
    # Lấy lịch tư vấn có sẵn của cố vấn
    lich_tu_van_list = LichTuVan.objects.filter(covan=covan).order_by('thoi_gian')
    
    if request.method == 'POST':
        lich_id = request.POST.get('lich_tu_van')
        noi_dung = request.POST.get('noi_dung_tu_van')
        
        if lich_id and noi_dung:
            lich = get_object_or_404(LichTuVan, id=lich_id, covan=covan)
            
            # Tạo phiếu tư vấn
            PhieuTuVan.objects.create(
                sinh_vien=sinhvien,
                covan=covan,
                lich_tu_van=lich,
                thoi_gian=lich.thoi_gian,
                noi_dung_tu_van=noi_dung
            )
            
            messages.success(request, 'Đăng ký lịch tư vấn thành công!')
            return redirect('tuvantuvan:lich_tu_van_sinhvien')
    
    context = {
        'lich_tu_van_list': lich_tu_van_list,
        'covan': covan
    }
    return render(request, 'tuvantuvan/dang_ky_lich.html', context)

@sinhvien_required
def lich_tu_van_sinhvien(request):
    """Lịch tư vấn của sinh viên"""
    sinhvien = request.user.sinhvien
    
    # Lịch tư vấn đã đăng ký
    phieu_tu_van = PhieuTuVan.objects.filter(
        sinh_vien=sinhvien
    ).select_related('covan', 'lich_tu_van').order_by('-thoi_gian')
    
    # Lịch sử đánh giá
    danh_gia = DanhGia.objects.filter(
        phieu__sinh_vien=sinhvien
    ).select_related('phieu')
    
    context = {
        'phieu_tu_van': phieu_tu_van,
        'danh_gia': danh_gia,
        'sinhvien': sinhvien
    }
    return render(request, 'tuvantuvan/lich_tu_van_sinhvien.html', context)

@sinhvien_required
def danh_gia_phieu_tu_van(request, phieu_id):
    """Sinh viên đánh giá phiếu tư vấn"""
    phieu = get_object_or_404(PhieuTuVan, id=phieu_id, sinh_vien=request.user.sinhvien)
    
    # Kiểm tra đã có đánh giá chưa
    danh_gia_exists = DanhGia.objects.filter(phieu=phieu).exists()
    
    if request.method == 'POST' and not danh_gia_exists:
        diem_danh_gia = request.POST.get('diem_danh_gia')
        nhan_xet = request.POST.get('nhan_xet', '')
        
        if diem_danh_gia:
            DanhGia.objects.create(
                phieu=phieu,
                diem_danh_gia=int(diem_danh_gia),
                nhan_xet=nhan_xet
            )
            
            messages.success(request, 'Đánh giá thành công!')
            return redirect('tuvantuvan:lich_tu_van_sinhvien')
    
    context = {
        'phieu': phieu,
        'danh_gia_exists': danh_gia_exists
    }
    return render(request, 'tuvantuvan/danh_gia_phieu.html', context)

@sinhvien_required
def thong_bao_sinhvien(request):
    """Thông báo cho sinh viên - phản hồi từ cố vấn"""
    sinhvien = request.user.sinhvien
    
    # Phiếu tư vấn đã có phản hồi
    phieu_co_phan_hoi = PhieuTuVan.objects.filter(
        sinh_vien=sinhvien,
        ket_qua__isnull=False
    ).select_related('covan').order_by('-thoi_gian')
    
    context = {
        'phieu_co_phan_hoi': phieu_co_phan_hoi,
        'sinhvien': sinhvien
    }
    return render(request, 'tuvantuvan/thong_bao_sinhvien.html', context)

@covan_required
def tao_lich_tu_van(request):
    """Cố vấn tạo lịch tư vấn"""
    covan = request.user.covan
    
    if request.method == 'POST':
        thoi_gian = request.POST.get('thoi_gian')
        dia_diem = request.POST.get('dia_diem')
        noi_dung_du_kien = request.POST.get('noi_dung_du_kien')
        
        if thoi_gian and dia_diem and noi_dung_du_kien:
            LichTuVan.objects.create(
                covan=covan,
                thoi_gian=thoi_gian,
                dia_diem=dia_diem,
                noi_dung_du_kien=noi_dung_du_kien
            )
            
            messages.success(request, 'Tạo lịch tư vấn thành công!')
            return redirect('covan:lich_tu_van')
    
    return render(request, 'tuvantuvan/tao_lich.html', {'covan': covan})

@sinhvien_required
def huy_lich_tu_van(request, phieu_id):
    """Sinh viên hủy lịch tư vấn (chỉ khi chưa có phản hồi)"""
    phieu = get_object_or_404(PhieuTuVan, id=phieu_id, sinh_vien=request.user.sinhvien)
    
    # Kiểm tra điều kiện hủy: chưa có phản hồi và trạng thái chờ phản hồi
    if phieu.ket_qua or phieu.trang_thai != 'cho_phan_hoi':
        messages.error(request, 'Không thể hủy lịch tư vấn này!')
        return redirect('tuvantuvan:lich_tu_van_sinhvien')
    
    if request.method == 'POST':
        phieu.trang_thai = 'da_huy'
        phieu.save()
        
        messages.success(request, 'Đã hủy lịch tư vấn thành công!')
        return redirect('tuvantuvan:lich_tu_van_sinhvien')
    
    context = {
        'phieu': phieu
    }
    return render(request, 'tuvantuvan/huy_lich.html', context)