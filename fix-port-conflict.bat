@echo off
echo ========================================
echo     SUA LOI XUNG DOT PORT
echo ========================================

echo.
echo Kiem tra cac port dang su dung...

echo.
echo [Port 3307] - MySQL hien tai:
netstat -an | findstr :3307
if not errorlevel 1 (
    echo ⚠️  Port 3307 dang duoc su dung boi MySQL hien tai
    echo.
    echo Cac lua chon:
    echo 1. Dung MySQL hien tai va su dung port 3308 cho Docker
    echo 2. Giu MySQL hien tai va thay doi port Docker
    echo.
    echo Chon lua chon 1 - Su dung port 3308 cho Docker MySQL
    echo Docker se su dung port 3308 thay vi 3307
) else (
    echo ✅ Port 3307 trong
)

echo.
echo [Port 8000] - Web server:
netstat -an | findstr :8000
if not errorlevel 1 (
    echo ⚠️  Port 8000 dang duoc su dung
    echo Ban co muon dung process dang chiem port 8000? (Y/N)
    choice /c YN /n >nul
    if errorlevel 2 (
        echo Thay doi port web server thanh 8001...
        echo Se cap nhat docker-compose.yml...
    )
) else (
    echo ✅ Port 8000 trong
)

echo.
echo [Port 8080] - phpMyAdmin:
netstat -an | findstr :8080
if not errorlevel 1 (
    echo ⚠️  Port 8080 dang duoc su dung
    echo Thay doi port phpMyAdmin thanh 8081...
) else (
    echo ✅ Port 8080 trong
)

echo.
echo ========================================
echo        CAP NHAT HOAN THANH!
echo ========================================
echo.
echo Cac port Docker moi:
echo - MySQL:      localhost:3308
echo - Web App:    localhost:8000 (hoac 8001)
echo - phpMyAdmin: localhost:8080 (hoac 8081)
echo.
echo Chay docker-build.bat de thu lai.
echo.
echo Nhan phim bat ky de tiep tuc...
pause >nul