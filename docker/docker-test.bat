@echo off
echo ========================================
echo       TEST HE THONG CVHT TVU
echo ========================================

echo.
echo [1/3] Kiem tra Docker Desktop...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Desktop chua duoc cai dat!
    echo Vui long cai dat Docker Desktop truoc.
    pause
    exit /b 1
)
echo ✅ Docker Desktop: OK

echo.
echo [2/3] Kiem tra Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose khong kha dung!
    pause
    exit /b 1
)
echo ✅ Docker Compose: OK

echo.
echo [3/3] Kiem tra cac port...
netstat -an | findstr :8000 >nul
if not errorlevel 1 (
    echo ⚠️  Port 8000 dang duoc su dung
    echo Ban co muon tiep tuc? (Y/N)
    choice /c YN /n >nul
    if errorlevel 2 exit /b 1
)

netstat -an | findstr :3308 >nul
if not errorlevel 1 (
    echo ⚠️  Port 3308 dang duoc su dung
    echo Ban co muon tiep tuc? (Y/N)
    choice /c YN /n >nul
    if errorlevel 2 exit /b 1
)

netstat -an | findstr :8080 >nul
if not errorlevel 1 (
    echo ⚠️  Port 8080 dang duoc su dung
    echo Ban co muon tiep tuc? (Y/N)
    choice /c YN /n >nul
    if errorlevel 2 exit /b 1
)

echo ✅ Cac port: OK

echo.
echo ========================================
echo        TAT CA KIEM TRA THANH CONG!
echo ========================================
echo.
echo He thong san sang de build va deploy.
echo Chay docker-build.bat de bat dau.
echo.
echo Nhan phim bat ky de tiep tuc...
pause >nul