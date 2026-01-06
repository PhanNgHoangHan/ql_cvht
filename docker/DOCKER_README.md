# 🐳 DOCKER DEPLOYMENT - HỆ THỐNG CVHT TVU (MySQL Local)

## 📋 Yêu cầu hệ thống

- **Docker Desktop** đã cài đặt và chạy
- **MySQL Workbench** hoặc **MySQL Server** đã cài đặt và chạy
- **Database**: cvht_db (sẽ tự động tạo)
- **MySQL Port**: 3307
- **MySQL User**: root với password: Nhanh1234@
- **Windows 10/11** hoặc **macOS** hoặc **Linux**
- **RAM**: Tối thiểu 4GB (khuyến nghị 8GB)
- **Disk**: Tối thiểu 2GB trống

## 🚀 Cách triển khai

### Phương pháp 1: Demo hoàn chỉnh (Windows)

```bash
# Demo 1-click (kiểm tra MySQL + tạo DB + build + start)
docker-demo.bat
```

### Phương pháp 2: Từng bước (Windows)

```bash
# 1. Kiểm tra MySQL local
check-mysql-local.bat

# 2. Tạo database (nếu chưa có)
create-database-local.bat

# 3. Build và khởi động
docker-build.bat
```

### Phương pháp 3: Thủ công

```bash
# Đảm bảo MySQL local đang chạy trên port 3307
# Build và khởi động
docker-compose up -d --build
```

## 🌐 Truy cập ứng dụng

Sau khi khởi động thành công:

- **🌍 Web App**: http://localhost:8000
- **🗄️ phpMyAdmin**: http://localhost:8080
- **📊 MySQL Local**: localhost:3307 (MySQL Workbench)

## 👤 Tài khoản mặc định

### Admin System
- **Username**: `admin`
- **Password**: `admin123`

### Database
- **Host**: `localhost:3308`
- **Database**: `cvht_db`
- **Username**: `cvht_user`
- **Password**: `cvht_password`

## 📁 Cấu trúc Docker

```
ql_cvht/
├── Dockerfile              # Docker image cho Django
├── docker-compose.yml      # Orchestration
├── docker-entrypoint.sh    # Script khởi động
├── .dockerignore           # Loại trừ files
├── mysql-init/             # Scripts khởi tạo DB
│   └── 01-init.sql
└── docker-*.bat            # Scripts Windows
```

## 🔧 Services

### 1. **MySQL Database** (`mysql`)
- **Image**: `mysql:8.0`
- **Port**: `3307:3306`
- **Volume**: `mysql_data`
- **Auto-init**: Tạo database và user

### 2. **Django Web** (`web`)
- **Build**: Từ Dockerfile
- **Port**: `8000:8000`
- **Depends**: MySQL
- **Auto-migrate**: Chạy migrations tự động

### 3. **phpMyAdmin** (`phpmyadmin`)
- **Image**: `phpmyadmin/phpmyadmin`
- **Port**: `8080:80`
- **Purpose**: Quản lý database

## 🛠️ Troubleshooting

### Lỗi thường gặp:

#### 1. **Port đã được sử dụng**
```bash
# Kiểm tra port
netstat -an | findstr :8000
netstat -an | findstr :3307

# Thay đổi port trong docker-compose.yml
ports:
  - "8001:8000"  # Thay vì 8000:8000
```

#### 2. **MySQL không khởi động**
```bash
# Xem logs MySQL
docker-compose logs mysql

# Xóa volume và tạo lại
docker-compose down -v
docker-compose up -d
```

#### 3. **Django không connect được MySQL**
```bash
# Kiểm tra network
docker-compose ps
docker network ls

# Restart web service
docker-compose restart web
```

#### 4. **Thiếu static files**
```bash
# Vào container và collect static
docker-compose exec web python manage.py collectstatic --noinput
```

## 📊 Monitoring

### Xem logs realtime:
```bash
# Tất cả services
docker-compose logs -f

# Chỉ web
docker-compose logs -f web

# Chỉ MySQL
docker-compose logs -f mysql
```

### Kiểm tra tài nguyên:
```bash
# Xem containers
docker-compose ps

# Xem tài nguyên
docker stats

# Vào container
docker-compose exec web bash
```

## 🔄 Cập nhật ứng dụng

```bash
# 1. Dừng containers
docker-compose down

# 2. Pull code mới (nếu có)
git pull

# 3. Rebuild và khởi động
docker-compose up -d --build

# 4. Chạy migrations (nếu cần)
docker-compose exec web python manage.py migrate
```

## 💾 Backup & Restore

### Backup Database:
```bash
# Backup toàn bộ
docker-compose exec mysql mysqldump -u cvht_user -pcvht_password cvht_db > backup.sql

# Backup với Docker
docker-compose exec mysql sh -c 'mysqldump -u cvht_user -pcvht_password cvht_db' > backup.sql
```

### Restore Database:
```bash
# Restore từ file
docker-compose exec -T mysql mysql -u cvht_user -pcvht_password cvht_db < backup.sql
```

## 🚀 Production Deployment

Để triển khai production, cần thay đổi:

### 1. **Environment Variables**
```yaml
environment:
  - DEBUG=False
  - SECRET_KEY=your-secret-key
  - ALLOWED_HOSTS=yourdomain.com
```

### 2. **SSL/HTTPS**
- Sử dụng reverse proxy (nginx)
- Cấu hình SSL certificates

### 3. **Database**
- Sử dụng managed database service
- Backup tự động

### 4. **Static Files**
- Sử dụng CDN
- Nginx serve static files

## 📞 Hỗ trợ

Nếu gặp vấn đề:

1. **Kiểm tra logs**: `docker-compose logs -f`
2. **Restart services**: `docker-compose restart`
3. **Clean rebuild**: `docker-compose down && docker-compose up -d --build`
4. **Xóa và tạo lại**: `docker-clean.bat` rồi `docker-build.bat`

---

**🎉 Chúc bạn triển khai thành công hệ thống CVHT TVU!**