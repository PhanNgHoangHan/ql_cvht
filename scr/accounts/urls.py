from django.urls import path
from .views import login_view, logout_view, change_password, forgot_password, reset_password_confirm, password_reset_success

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password, name='change_password'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password_confirm, name='reset_password_confirm'),
    path('password-reset-success/', password_reset_success, name='password_reset_success'),
]
