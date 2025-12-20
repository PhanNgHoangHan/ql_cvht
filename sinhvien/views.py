from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_sinhvien(user):
    return user.groups.filter(name='SINH_VIEN').exists()

@login_required
@user_passes_test(is_sinhvien)
def dashboard(request):
    return render(request, 'sinhvien/dashboard.html')
