@echo off
echo ========================================
echo      DUNG MYSQL LOCAL (NEU CAN)
echo ========================================

echo.
echo CANH BAO: Script nay se dung MySQL server dang chay tren may ban!
echo Chi chay neu ban muon su dung Docker MySQL thay vi MySQL local.
echo.
echo Ban co chac chan muon dung MySQL local? (Y/N)
choice /c YN /n >nul
if errorlevel 2 goto :cancel

echo.
echo Dang dung MySQL service...

:: Dừng MySQL service
net stop MySQL80 2>nul
if errorlevel 1 (
    net stop MySQL 2>nul
    if errorlevel 1 (
        echo ⚠️  Khong tim thay MySQL service hoac khong co quyen admin
        echo Vui long:
        echo 1. Chay Command Prompt as Administrator
        echo 2. Hoac dung MySQL Workbench/phpMyAdmin de disconnect
        echo 3. Hoac su dung Task Manager de tat mysqld.exe
        goto :end
    )
)

echo ✅ Da dung MySQL service thanh cong!
echo.
echo Gio ban co the chay Docker MySQL tren port 3307.
echo Chay docker-build.bat de khoi dong Docker.
goto :end

:cancel
echo.
echo Huy thao tac. MySQL local van dang chay.
echo Docker se su dung port 3308 thay vi 3307.

:end
echo.
echo Nhan phim bat ky de tiep tuc...
pause >nul