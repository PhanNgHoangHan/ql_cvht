@echo off
echo ===== KHOI CHAY HE THONG QUAN LY CVHT =====
echo Giao dien da duoc nang cap voi Bootstrap va CSS tuong tac

echo 1. Chay migrations...
python manage.py makemigrations
python manage.py migrate

echo 2. Thu thap static files...
python manage.py collectstatic --noinput

echo 3. Xoa va tao lai du lieu mau...
python reset_data.py

echo 4. Kiem tra du lieu...
python test_data.py

echo 5. Test chuc nang bao cao...
python test_report.py

echo 6. Khoi dong server...
echo.
echo ========================================
echo   THONG TIN TRUY CAP HE THONG
echo ========================================
echo URL: http://localhost:8000/login/
echo.
echo TAI KHOAN DEMO:
echo - Admin: admin / admin123
echo - Co van: covan01 / 123456  
echo - Sinh vien: sv001 / 123456 (co 1 mon "Chua Dat")
echo - Sinh vien: sv002 / 123456 (co 2 mon "Chua Dat")  
echo - Sinh vien: sv003 / 123456 (tat ca mon "Dat")
echo.
echo TINH NANG MOI:
echo - Giao dien Bootstrap 5 chuyen nghiep
echo - Bieu do thong ke tuong tac
echo - Trang in bao cao dep theo mau truong DH
echo - Navigation responsive va user-friendly
echo - Dashboard voi cac card thong ke truc quan
echo - Bao cao chi tiet da sua loi
echo ========================================
echo.
python manage.py runserver