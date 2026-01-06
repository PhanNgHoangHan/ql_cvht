@echo off
echo ========================================
echo       KHAC PHUC NHANH LOI PORT
echo ========================================

echo.
echo Dang khac phuc loi xung dot port 3307...

echo.
echo [1/3] Dung cac Docker container cu...
docker-compose down 2>nul

echo.
echo [2/3] Xoa cac container va image cu...
docker container prune -f 2>nul
docker rmi ql_cvht-web 2>nul

echo.
echo [3/3] Khoi dong lai voi port moi (3308)...
docker-compose up -d --build

echo.
echo ========================================
echo         KHAC PHUC HOAN THANH!
echo ========================================
echo.
echo Port moi da duoc su dung:
echo - MySQL Docker: localhost:3308 (thay vi 3307)
echo - Web App:      localhost:8000
echo - phpMyAdmin:   localhost:8080
echo.
echo MySQL local van co the chay tren port 3307
echo Docker MySQL chay tren port 3308
echo.
echo Kiem tra trang thai:
docker-compose ps

echo.
echo Nhan phim bat ky de tiep tuc...
pause >nul