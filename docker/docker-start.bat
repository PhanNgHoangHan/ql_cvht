@echo off
echo ========================================
echo     KHOI DONG HE THONG CVHT TVU
echo ========================================

echo.
echo Khoi dong cac Docker containers...
docker-compose up -d

echo.
echo Kiem tra trang thai services...
docker-compose ps

echo.
echo ========================================
echo         KHOI DONG HOAN THANH!
echo ========================================
echo.
echo Truy cap ung dung:
echo - Web App:     http://localhost:8000
echo - phpMyAdmin:  http://localhost:8080
echo.
echo Xem logs:
echo - docker-compose logs web
echo - docker-compose logs mysql
echo.
echo Nhan phim bat ky de tiep tuc...
pause >nul