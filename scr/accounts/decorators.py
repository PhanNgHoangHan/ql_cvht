from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from functools import wraps

def is_sinhvien(user):
    """Kiểm tra user có thuộc nhóm SINH_VIEN không"""
    return user.groups.filter(name='SINH_VIEN').exists()

def is_covan(user):
    """Kiểm tra user có thuộc nhóm CO_VAN không"""
    return user.groups.filter(name='CO_VAN').exists()

def sinhvien_required(view_func):
    """Decorator yêu cầu user phải là sinh viên"""
    @wraps(view_func)
    @login_required
    @user_passes_test(is_sinhvien)
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper

def covan_required(view_func):
    """Decorator yêu cầu user phải là cố vấn"""
    @wraps(view_func)
    @login_required
    @user_passes_test(is_covan)
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper

def sinhvien_or_covan_required(view_func):
    """Decorator cho phép cả sinh viên và cố vấn truy cập"""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not (is_sinhvien(request.user) or is_covan(request.user)):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def check_sinhvien_access(view_func):
    """
    Decorator kiểm tra quyền truy cập thông tin sinh viên:
    - Sinh viên chỉ xem được thông tin của chính mình
    - Cố vấn chỉ xem được sinh viên trong lớp mình phụ trách
    """
    @wraps(view_func)
    @sinhvien_or_covan_required
    def wrapper(request, *args, **kwargs):
        from sinhvien.models import SinhVien
        
        # Lấy pk của sinh viên từ URL
        sinhvien_pk = kwargs.get('pk')
        if sinhvien_pk:
            sinhvien = get_object_or_404(SinhVien, pk=sinhvien_pk)
            
            # Nếu là sinh viên, chỉ được xem thông tin của chính mình
            if is_sinhvien(request.user):
                if not hasattr(request.user, 'sinhvien') or request.user.sinhvien != sinhvien:
                    raise PermissionDenied
            
            # Nếu là cố vấn, chỉ được xem sinh viên trong lớp mình phụ trách
            elif is_covan(request.user):
                if not hasattr(request.user, 'covan') or request.user.covan.lop != sinhvien.lop:
                    raise PermissionDenied
        
        return view_func(request, *args, **kwargs)
    return wrapper