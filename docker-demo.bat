@echo off
echo ========================================
echo   DEMO HE THONG CVHT TVU - MYSQL LOCAL
echo ========================================

echo.
echo Chuan bi demo he thong voi MySQL Workbench...

echo.
echo [1/6] Kiem tra MySQL local...
call check-mysql-local.bat
if errorlevel 1 exit /b 1

echo.
echo [2/6] Tao database neu chua co...
call create-database-local.bat

echo.
echo [3/6] Kiem tra Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Desktop chua duoc cai dat!
    pause
    exit /b 1
)
echo ✅ Docker Desktop: OK

echo.
echo [4/6] Build va khoi dong he thong...
call docker-build.bat

echo.
echo [5/6] Cho he thong khoi dong hoan toan...
timeout /t 30 /nobreak >nul

echo.
echo [6/6] Mo trinh duyet...
start http://localhost:8000
start http://localhost:8080

echo.
echo ========================================
echo           DEMO HOAN THANH!
echo ========================================
echo.
echo Cac URL da duoc mo:
echo - 🌍 Web App:     http://localhost:8000
echo - 🗄️ phpMyAdmin:  http://localhost:8080
echo.
echo Database:
echo - MySQL local:   localhost:3307 (MySQL Workbench)
echo - Database:      cvht_db
echo - User:          root
echo.
echo Tai khoan demo:
echo - Admin:    admin / admin123
echo.
echo Huong dan su dung:
echo 1. Dang nhap admin panel: /admin/
echo 2. Tao nhom SINH_VIEN va CO_VAN (neu chua co)
echo 3. Tao user va gan vao nhom
echo 4. Dang nhap he thong chinh
echo.
echo Du lieu se duoc luu trong MySQL Workbench cua ban!
echo.
echo Nhan phim bat ky de tiep tuc...
pause >nul