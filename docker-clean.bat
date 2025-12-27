@echo off
echo ========================================
echo      XOA HOAN TOAN HE THONG
echo ========================================

echo.
echo CANH BAO: Thao tac nay se xoa tat ca du lieu!
echo Nhan Y de tiep tuc, phim khac de huy...
choice /c YN /n >nul
if errorlevel 2 goto :cancel

echo.
echo [1/4] Dung cac containers...
docker-compose down

echo.
echo [2/4] Xoa volumes (du lieu database)...
docker-compose down -v

echo.
echo [3/4] Xoa images...
docker rmi ql_cvht-web 2>nul
docker rmi mysql:8.0 2>nul
docker rmi phpmyadmin/phpmyadmin 2>nul

echo.
echo [4/4] Xoa networks...
docker network prune -f

echo.
echo ========================================
echo         XOA HOAN THANH!
echo ========================================
echo.
echo Tat ca du lieu da bi xoa. De cai dat lai:
echo 1. Chay docker-build.bat
echo 2. Hoac docker-start.bat
echo.
goto :end

:cancel
echo.
echo Huy thao tac xoa.
echo.

:end
echo Nhan phim bat ky de tiep tuc...
pause >nul