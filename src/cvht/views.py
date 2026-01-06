from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required(login_url='/login/')
def home_view(request):
    """Điều hướng dashboard theo role của user"""
    user = request.user
    
    # Điều hướng theo nhóm
    if user.groups.filter(name='SINH_VIEN').exists():
        return redirect('sinhvien:dashboard')
    elif user.groups.filter(name='CO_VAN').exists():
        return redirect('covan:dashboard')
    
    # Nếu không thuộc nhóm nào, hiển thị trang mặc định
    return render(request, 'dashboard/home.html')
