@echo off
echo ========================================
echo    KIEM TRA MYSQL LOCAL WORKBENCH
echo ========================================

echo.
echo [1/4] Kiem tra MySQL service dang chay...
sc query MySQL80 | findstr "RUNNING" >nul
if errorlevel 1 (
    sc query MySQL | findstr "RUNNING" >nul
    if errorlevel 1 (
        echo ❌ MySQL service khong chay!
        echo Vui long khoi dong MySQL service:
        echo 1. Mo Services.msc
        echo 2. Tim MySQL80 hoac MySQL
        echo 3. Click Start
        echo.
        echo Hoac khoi dong MySQL Workbench va ket noi
        pause
        exit /b 1
    ) else (
        echo ✅ MySQL service dang chay
    )
) else (
    echo ✅ MySQL80 service dang chay
)

echo.
echo [2/4] Kiem tra port 3307...
netstat -an | findstr :3307 >nul
if errorlevel 1 (
    echo ❌ MySQL khong lang nghe tren port 3307!
    echo Kiem tra cau hinh MySQL:
    echo 1. Mo MySQL Workbench
    echo 2. Kiem tra connection port
    echo 3. Hoac sua port trong docker-compose.yml
    pause
    exit /b 1
) else (
    echo ✅ MySQL dang lang nghe tren port 3307
)

echo.
echo [3/4] Kiem tra database cvht_db...
mysql -h localhost -P 3307 -u root -pNhanh1234@ -e "USE cvht_db; SHOW TABLES;" 2>nul
if errorlevel 1 (
    echo ⚠️  Database cvht_db chua ton tai hoac khong ket noi duoc
    echo Se tao database khi chay Docker
) else (
    echo ✅ Database cvht_db da ton tai
)

echo.
echo [4/4] Kiem tra user root...
mysql -h localhost -P 3307 -u root -pNhanh1234@ -e "SELECT 1;" 2>nul
if errorlevel 1 (
    echo ❌ Khong ket noi duoc voi user root!
    echo Kiem tra:
    echo 1. Password: Nhanh1234@
    echo 2. User root co quyen truy cap
    echo 3. MySQL cho phep ket noi tu localhost
    pause
    exit /b 1
) else (
    echo ✅ Ket noi thanh cong voi user root
)

echo.
echo ========================================
echo      MYSQL LOCAL SAN SANG!
echo ========================================
echo.
echo Thong tin ket noi:
echo - Host: localhost
echo - Port: 3307
echo - User: root
echo - Password: Nhanh1234@
echo - Database: cvht_db (se tao neu chua co)
echo.
echo Docker co the ket noi voi MySQL local cua ban!
echo Chay docker-build.bat de khoi dong.
echo.
echo Nhan phim bat ky de tiep tuc...
pause >nul