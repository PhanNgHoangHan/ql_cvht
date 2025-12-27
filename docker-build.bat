@echo off
echo ========================================
echo  DOCKER BUILD - KET NOI MYSQL LOCAL
echo ========================================

echo.
echo [1/5] Kiem tra MySQL local...
call check-mysql-local.bat
if errorlevel 1 (
    echo ❌ MySQL local chua san sang!
    echo Vui long khoi dong MySQL Workbench truoc.
    pause
    exit /b 1
)

echo.
echo [2/5] Dung cac container cu (neu co)...
docker-compose down

echo.
echo [3/5] Xoa image cu (neu co)...
docker rmi ql_cvht-web 2>nul

echo.
echo [4/5] Build Docker image moi...
docker-compose build --no-cache

echo.
echo [5/5] Khoi dong cac services...
docker-compose up -d

echo.
echo ========================================
echo           BUILD HOAN THANH!
echo ========================================
echo.
echo Cac services dang chay:
docker-compose ps

echo.
echo Truy cap ung dung:
echo - Web App:     http://localhost:8000
echo - phpMyAdmin:  http://localhost:8080
echo.
echo Ket noi database:
echo - MySQL local: localhost:3307 (MySQL Workbench)
echo - Database:    cvht_db
echo - User:        root
echo.
echo Tai khoan ung dung:
echo - Username: admin
echo - Password: admin123
echo.
echo Nhan phim bat ky de tiep tuc...
pause >nul