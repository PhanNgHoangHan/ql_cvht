@echo off
echo ========================================
echo      DUNG HE THONG CVHT TVU
echo ========================================

echo.
echo Dung cac Docker containers...
docker-compose down

echo.
echo Kiem tra trang thai...
docker-compose ps

echo.
echo ========================================
echo          DUNG HOAN THANH!
echo ========================================
echo.
echo De khoi dong lai, chay: docker-start.bat
echo De xoa hoan toan, chay: docker-clean.bat
echo.
echo Nhan phim bat ky de tiep tuc...
pause >nul