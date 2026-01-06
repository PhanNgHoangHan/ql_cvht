# 🗄️ HƯỚNG DẪN SETUP MYSQL WORKBENCH

## 📋 Yêu cầu

Docker sẽ kết nối với MySQL Workbench đã có sẵn trên máy bạn thay vì tạo MySQL container riêng.

## ⚙️ Cấu hình MySQL Workbench

### 1. **Kiểm tra MySQL Service**
- Mở **Services** (services.msc)
- Tìm **MySQL80** hoặc **MySQL**
- Đảm bảo service đang **Running**

### 2. **Kiểm tra Connection trong MySQL Workbench**
- Mở **MySQL Workbench**
- Connection name: `Local instance MySQL80` (hoặc tương tự)
- **Hostname**: `localhost` hoặc `127.0.0.1`
- **Port**: `3307` (quan trọng!)
- **Username**: `root`
- **Password**: `Nhanh1234@`

### 3. **Test Connection**
- Click **Test Connection**
- Phải thành công trước khi chạy Docker

## 🔧 Cấu hình cần thiết

### Thông tin kết nối:
```
Host: localhost
Port: 3307
User: root
Password: Nhanh1234@
Database: cvht_db (sẽ tự động tạo)
```

### Nếu port khác 3307:
1. Kiểm tra port trong MySQL Workbench
2. Cập nhật `docker-compose.yml`:
```yaml
environment:
  - DB_PORT=YOUR_PORT  # Thay YOUR_PORT bằng port thực tế
```

## 🚀 Các bước triển khai

### 1. **Kiểm tra MySQL Local**
```bash
# Chạy script kiểm tra
check-mysql-local.bat
```

### 2. **Tạo Database (nếu cần)**
```bash
# Tạo database cvht_db
create-database-local.bat
```

### 3. **Khởi động Docker**
```bash
# Build và start
docker-build.bat

# Hoặc demo hoàn chỉnh
docker-demo.bat
```

## 🔍 Troubleshooting

### Lỗi thường gặp:

#### 1. **MySQL Service không chạy**
```bash
# Khởi động service
net start MySQL80
# hoặc
net start MySQL
```

#### 2. **Port 3307 không mở**
- Kiểm tra MySQL config file (my.ini)
- Tìm dòng `port = 3307`
- Restart MySQL service

#### 3. **Không kết nối được từ Docker**
- Kiểm tra MySQL bind-address
- Đảm bảo MySQL cho phép kết nối từ localhost
- Kiểm tra firewall

#### 4. **Password không đúng**
- Đảm bảo password root là: `Nhanh1234@`
- Hoặc cập nhật password trong `docker-compose.yml`

## 📊 Quản lý dữ liệu

### Xem dữ liệu:
- Mở **MySQL Workbench**
- Kết nối với **Local instance**
- Chọn database **cvht_db**
- Xem các bảng Django đã tạo

### Backup dữ liệu:
```sql
-- Trong MySQL Workbench
mysqldump -u root -p cvht_db > backup.sql
```

### Restore dữ liệu:
```sql
-- Trong MySQL Workbench
mysql -u root -p cvht_db < backup.sql
```

## ✅ Kiểm tra thành công

Sau khi setup thành công:

1. **MySQL Workbench** kết nối được với `localhost:3307`
2. **Database cvht_db** đã được tạo
3. **Docker containers** chạy thành công:
   - Web app: http://localhost:8000
   - phpMyAdmin: http://localhost:8080
4. **phpMyAdmin** kết nối được với MySQL local

## 🎯 Lợi ích của cách này

- ✅ **Dữ liệu persistent**: Không mất khi xóa Docker containers
- ✅ **Quản lý dễ dàng**: Sử dụng MySQL Workbench quen thuộc
- ✅ **Performance tốt**: MySQL chạy native trên host
- ✅ **Backup dễ dàng**: Sử dụng tools có sẵn của MySQL
- ✅ **Development friendly**: Có thể xem/sửa dữ liệu trực tiếp

---

**🎉 Bây giờ bạn có thể sử dụng MySQL Workbench để quản lý dữ liệu và Docker để chạy ứng dụng!**