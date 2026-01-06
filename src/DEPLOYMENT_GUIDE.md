# 🚀 HƯỚNG DẪN TRIỂN KHAI DOCKER - HỆ THỐNG CVHT TVU

## 📦 Tổng quan

Dự án đã được đóng gói hoàn chỉnh với Docker để triển khai dễ dàng trên bất kỳ máy nào có Docker Desktop.

## 🎯 Triển khai nhanh (1 click)

### Windows:
```bash
# Chạy demo hoàn chỉnh
docker-demo.bat

# Hoặc chỉ build và khởi động
docker-build.bat
```

### Linux/macOS:
```bash
# Build và khởi động
docker-compose up -d --build

# Xem logs
docker-compose logs -f
```

## 📋 Checklist triển khai

### ✅ Trước khi bắt đầu:
- [ ] Docker Desktop đã cài đặt và chạy
- [ ] Port 8000, 3307, 8080 không bị chiếm dụng
- [ ] Có ít nhất 4GB RAM trống
- [ ] Có ít nhất 2GB disk trống

### ✅ Các bước triển khai:
1. [ ] Clone/download source code
2. [ ] Mở terminal trong thư mục dự án
3. [ ] Chạy `docker-test.bat` để kiểm tra
4. [ ] Chạy `docker-build.bat` để build và khởi động
5. [ ] Truy cập http://localhost:8000
6. [ ] Đăng nhập admin panel: admin/admin123

## 🌐 Các URL sau khi triển khai

| Service | URL | Mô tả |
|---------|-----|-------|
| **Web App** | http://localhost:8000 | Ứng dụng chính |
| **Admin Panel** | http://localhost:8000/admin/ | Quản trị hệ thống |
| **phpMyAdmin** | http://localhost:8080 | Quản lý database |

## 👤 Tài khoản mặc định

### System Admin:
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Superuser (tất cả quyền)

### Database:
- **Host**: `localhost:3308`
- **Database**: `cvht_db`
- **Username**: `cvht_user`
- **Password**: `cvht_password`

## 🔧 Quản lý hệ thống

### Khởi động/Dừng:
```bash
# Khởi động
docker-start.bat

# Dừng
docker-stop.bat

# Xóa hoàn toàn (cẩn thận!)
docker-clean.bat
```

### Xem logs:
```bash
# Tất cả services
docker-compose logs -f

# Chỉ web app
docker-compose logs -f web

# Chỉ database
docker-compose logs -f mysql
```

### Backup database:
```bash
# Backup
docker-compose exec mysql mysqldump -u cvht_user -pcvht_password cvht_db > backup.sql

# Restore
docker-compose exec -T mysql mysql -u cvht_user -pcvht_password cvht_db < backup.sql
```

## 🏗️ Cấu trúc Docker

```
ql_cvht/
├── 🐳 Docker Files
│   ├── Dockerfile              # Image definition
│   ├── docker-compose.yml      # Services orchestration
│   ├── docker-entrypoint.sh    # Startup script
│   └── .dockerignore           # Exclude files
│
├── 🗄️ Database Init
│   └── mysql-init/
│       └── 01-init.sql         # DB initialization
│
├── 🚀 Deployment Scripts
│   ├── docker-build.bat        # Build & start
│   ├── docker-start.bat        # Start services
│   ├── docker-stop.bat         # Stop services
│   ├── docker-clean.bat        # Clean all
│   ├── docker-test.bat         # Test environment
│   └── docker-demo.bat         # Full demo
│
├── ⚙️ Configuration
│   ├── .env.example            # Environment template
│   ├── requirements.txt        # Python dependencies
│   └── docker-init-data.py     # Data initialization
│
└── 📚 Documentation
    ├── DOCKER_README.md        # Docker guide
    ├── DEPLOYMENT_GUIDE.md     # This file
    └── FEATURES_SUMMARY.md     # Features overview
```

## 🔍 Troubleshooting

### Vấn đề thường gặp:

#### 1. **Docker Desktop không chạy**
```bash
# Khởi động Docker Desktop
# Đợi icon Docker trong system tray chuyển xanh
```

#### 2. **Port bị chiếm dụng**
```bash
# Kiểm tra port
netstat -an | findstr :8000

# Thay đổi port trong docker-compose.yml
ports:
  - "8001:8000"  # Thay vì 8000:8000
```

#### 3. **MySQL không khởi động**
```bash
# Xem logs
docker-compose logs mysql

# Xóa volume và tạo lại
docker-compose down -v
docker-compose up -d
```

#### 4. **Web app không kết nối database**
```bash
# Restart web service
docker-compose restart web

# Hoặc rebuild
docker-compose up -d --build
```

#### 5. **Thiếu static files**
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

## 🎯 Sau khi triển khai thành công

### 1. **Tạo dữ liệu mẫu**
- Truy cập admin panel: http://localhost:8000/admin/
- Đăng nhập: admin/admin123
- Tạo các nhóm: SINH_VIEN, CO_VAN
- Tạo users và gán vào nhóm
- Tạo dữ liệu mẫu (khoa, lớp, sinh viên, cố vấn)

### 2. **Test các tính năng**
- Đăng nhập với tài khoản sinh viên
- Đăng ký tư vấn, hủy lịch
- Đăng nhập với tài khoản cố vấn
- Phản hồi tư vấn, xem thống kê
- Test quên mật khẩu với email

### 3. **Cấu hình email (nếu cần)**
- Cập nhật thông tin email trong settings.py
- Test chức năng gửi email

## 🌟 Tính năng đã triển khai

✅ **Hoàn chỉnh 100%**:
- Hệ thống đăng nhập/phân quyền
- Dashboard sinh viên/cố vấn
- Quản lý tư vấn (đăng ký, hủy, phản hồi)
- Thống kê và báo cáo
- Quên mật khẩu với email
- Giao diện responsive
- Docker deployment

## 🚀 Production Ready

Hệ thống đã sẵn sàng cho production với:
- ✅ Containerized deployment
- ✅ Database persistence
- ✅ Static files handling
- ✅ Environment configuration
- ✅ Health checks
- ✅ Logging
- ✅ Backup/restore procedures

---

## 🎉 Chúc mừng!

Bạn đã triển khai thành công **Hệ thống quản lý cố vấn học tập TVU** với Docker!

**Liên hệ hỗ trợ**: Nếu gặp vấn đề, hãy kiểm tra logs và tham khảo troubleshooting guide.