from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Điều hướng theo group
            if user.groups.filter(name='SINH_VIEN').exists():
                return redirect('sinhvien:dashboard')

            if user.groups.filter(name='CO_VAN').exists():
                return redirect('covan:dashboard')

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
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

@login_required
def change_password(request):
    """Thay đổi mật khẩu"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Giữ session sau khi đổi mật khẩu
            messages.success(request, 'Mật khẩu đã được thay đổi thành công!')
            return redirect('change_password')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin!')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'auth/change_password.html', {'form': form})
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
import hashlib

# Tạm thời lưu mã xác nhận trong memory (production nên dùng Redis/Database)
reset_codes = {}

def forgot_password(request):
    """Quên mật khẩu - gửi mã xác nhận"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        
        print(f"DEBUG: Username nhập: '{username}', Email nhập: '{email}'")
        
        user = None
        
        # Tìm user theo username trước
        if username:
            try:
                user = User.objects.get(username=username)
                print(f"DEBUG: Tìm thấy user {user.username}, email hiện tại: '{user.email}'")
                
                # Nếu user không có email, tạo email tạm thời
                if not user.email:
                    user.email = f"{username}@tvu.edu.vn"
                    user.save()
                    print(f"DEBUG: Tạo email tạm thời: {user.email}")
                    
            except User.DoesNotExist:
                print(f"DEBUG: Không tìm thấy user với username: {username}")
        
        if user:
            # Tạo mã xác nhận 6 số
            reset_code = get_random_string(6, '0123456789')
            print(f"DEBUG: Tạo mã xác nhận: {reset_code}")
            
            # Lưu mã xác nhận với thời gian hết hạn (15 phút)
            reset_codes[user.username] = {
                'code': reset_code,
                'expires': timezone.now() + timedelta(minutes=15),
                'user_id': user.id
            }
            
            # Gửi email thật
            try:
                subject = 'Mã xác nhận đặt lại mật khẩu - Hệ thống TVU'
                message = f'''
Xin chào {user.get_full_name() or user.username},

Bạn đã yêu cầu đặt lại mật khẩu cho tài khoản của mình.

Mã xác nhận của bạn là: {reset_code}

Mã này sẽ hết hạn sau 15 phút.

Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.

Trân trọng,
Hệ thống quản lý cố vấn học tập
Trường Đại học Trà Vinh
                '''
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                
                messages.success(request, f'Mã xác nhận đã được gửi đến email: {user.email}')
                print(f"DEBUG: Email đã gửi thành công đến {user.email} với mã: {reset_code}")
                
            except Exception as e:
                # Nếu gửi email thất bại, vẫn hiển thị mã để development
                messages.warning(request, f'Không thể gửi email. Mã xác nhận của bạn là: {reset_code}')
                print(f"DEBUG: Lỗi gửi email: {e}")
                print(f"DEBUG: Mã xác nhận: {reset_code}")
            
            return redirect('reset_password_confirm')
        else:
            messages.error(request, 'Không tìm thấy tài khoản với thông tin này!')
            print("DEBUG: Không tìm thấy user nào")
    
    return render(request, 'auth/forgot_password.html')

def reset_password_confirm(request):
    """Xác nhận mã và đặt lại mật khẩu"""
    if request.method == 'POST':
        username = request.POST.get('username')
        reset_code = request.POST.get('reset_code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Kiểm tra mã xác nhận
        if username in reset_codes:
            stored_data = reset_codes[username]
            
            # Kiểm tra mã và thời gian hết hạn
            if (stored_data['code'] == reset_code and 
                timezone.now() < stored_data['expires']):
                
                # Kiểm tra mật khẩu
                if new_password != confirm_password:
                    messages.error(request, 'Mật khẩu xác nhận không khớp!')
                elif len(new_password) < 8:
                    messages.error(request, 'Mật khẩu phải có ít nhất 8 ký tự!')
                else:
                    # Đặt lại mật khẩu
                    try:
                        user = User.objects.get(id=stored_data['user_id'])
                        user.set_password(new_password)
                        user.save()
                        
                        # Xóa mã xác nhận đã sử dụng
                        del reset_codes[username]
                        
                        # Gửi email thông báo thành công
                        try:
                            subject = 'Mật khẩu đã được đặt lại thành công - Hệ thống TVU'
                            message = f'''
Xin chào {user.get_full_name() or user.username},

Mật khẩu của bạn đã được đặt lại thành công vào lúc {timezone.now().strftime("%d/%m/%Y %H:%M:%S")}.

Thông tin tài khoản:
- Tên đăng nhập: {user.username}
- Email: {user.email}

Bạn có thể đăng nhập ngay bây giờ với mật khẩu mới.

Nếu bạn không thực hiện thay đổi này, vui lòng liên hệ với quản trị viên ngay lập tức.

Trân trọng,
Hệ thống quản lý cố vấn học tập
Trường Đại học Trà Vinh
                            '''
                            
                            send_mail(
                                subject,
                                message,
                                settings.DEFAULT_FROM_EMAIL,
                                [user.email],
                                fail_silently=True,  # Không làm gián đoạn nếu email thất bại
                            )
                            print(f"DEBUG: Email thông báo thành công đã gửi đến {user.email}")
                            
                        except Exception as e:
                            print(f"DEBUG: Lỗi gửi email thông báo: {e}")
                        
                        messages.success(request, 
                            f'🎉 Mật khẩu đã được đặt lại thành công! '
                            f'Email xác nhận đã được gửi đến {user.email}.')
                        return redirect('password_reset_success')
                        
                    except User.DoesNotExist:
                        messages.error(request, 'Có lỗi xảy ra, vui lòng thử lại!')
            else:
                messages.error(request, 'Mã xác nhận không đúng hoặc đã hết hạn!')
        else:
            messages.error(request, 'Không tìm thấy yêu cầu đặt lại mật khẩu!')
    
    return render(request, 'auth/reset_password_confirm.html')

def password_reset_success(request):
    """Trang thông báo đặt lại mật khẩu thành công"""
    return render(request, 'auth/password_reset_success.html')