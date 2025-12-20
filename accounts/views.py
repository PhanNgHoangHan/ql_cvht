from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Điều hướng theo group
            if user.groups.filter(name='SINH_VIEN').exists():
                return redirect('sv_dashboard')

            if user.groups.filter(name='CO_VAN').exists():
                return redirect('cv_dashboard')

            return redirect('dashboard')
        else:
            return render(request, 'auth/login.html', {
                'error': 'Sai tài khoản hoặc mật khẩu'
            })

    return render(request, 'auth/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
