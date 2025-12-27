@echo off
echo ========================================
echo    TAO DATABASE TRONG MYSQL LOCAL
echo ========================================

echo.
echo Dang tao database cvht_db trong MySQL local...

echo.
echo [1/2] Kiem tra ket noi MySQL...
mysql -h localhost -P 3307 -u root -pNhanh1234@ -e "SELECT 1;" 2>nul
if errorlevel 1 (
    echo ❌ Khong ket noi duoc MySQL local!
    echo Kiem tra:
    echo 1. MySQL service dang chay
    echo 2. Port 3307 dung
    echo 3. Password: Nhanh1234@
    pause
    exit /b 1
)
echo ✅ Ket noi MySQL thanh cong

echo.
echo [2/2] Tao database va cau hinh...
mysql -h localhost -P 3307 -u root -pNhanh1234@ << EOF
-- Tao database neu chua co
CREATE DATABASE IF NOT EXISTS cvht_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Su dung database
USE cvht_db;

-- Hien thi thong bao
SELECT 'Database cvht_db da duoc tao thanh cong!' as message;

-- Hien thi cac database hien co
SHOW DATABASES;
EOF

if errorlevel 1 (
    echo ❌ Loi tao database!
    pause
    exit /b 1
)

echo.
echo ========================================
echo        TAO DATABASE THANH CONG!
echo ========================================
echo.
echo Database cvht_db da san sang trong MySQL local.
echo Ban co the:
echo 1. Mo MySQL Workbench de xem database
echo 2. Chay docker-build.bat de khoi dong ung dung
echo 3. Django se tu dong tao cac bang khi chay migrations
echo.
echo Nhan phim bat ky de tiep tuc...
pause >nul