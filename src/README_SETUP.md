# Hướng dẫn cài đặt và chạy hệ thống Quản lý CVHT

## Tính năng giao diện mới

### 🎨 Giao diện Bootstrap 5 chuyên nghiệp
- Theme giáo dục với màu sắc chuyên nghiệp
- Responsive design cho mọi thiết bị
- Icons Bootstrap đẹp mắt
- Animation và hiệu ứng mượt mà

### 📊 Dashboard trực quan
- Cards thống kê với gradient đẹp
- Biểu đồ tương tác với Chart.js
- Layout grid responsive
- Quick actions với icons

### 🖨️ Trang in báo cáo chuyên nghiệp
- Header trường đại học chuẩn
- Bảng dữ liệu được format đẹp
- Phần chữ ký và thông tin báo cáo
- CSS print tối ưu

### 🔐 Trang đăng nhập hiện đại
- Gradient background với animation
- Form đăng nhập 2 cột đẹp mắt
- Thông tin demo accounts
- Responsive mobile-friendly

## 1. Cài đặt môi trường

```bash
# Cài đặt các package cần thiết
pip install -r requirements.txt
```

## 2. Cấu hình database

Đảm bảo MySQL đang chạy và cập nhật thông tin kết nối trong `ql_cvht/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cvht_db',
        'USER': 'root',
        'PASSWORD': 'Nhanh1234@',
        'HOST': '127.0.0.1',
        'PORT': '3307',
    }
}
```

## 3. Chạy hệ thống nhanh

```bash
# Chạy script tự động (Windows)
run_system.bat

# Hoặc chạy từng bước thủ công
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python reset_data.py
python manage.py runserver
```

## 4. Truy cập hệ thống

- **URL**: http://localhost:8000/login/
- **Tài khoản Admin**: `admin` / `admin123`
- **Tài khoản Cố vấn**: `covan01` / `123456`
- **Tài khoản Sinh viên**: `sv001` / `123456` (có môn chưa đạt)

## 5. Tính năng hệ thống

### Sinh viên (SINH_VIEN):
- ✅ Dashboard cá nhân với thống kê trực quan
- ✅ Xem thông tin cá nhân và kết quả học tập
- ✅ Đăng ký lịch tư vấn với giao diện đẹp
- ✅ Xem thông báo phản hồi từ cố vấn
- ✅ Đánh giá buổi tư vấn
- ✅ Biểu đồ thống kê điểm số (doughnut chart)

### Cố vấn (CO_VAN):
- ✅ Dashboard quản lý với cards thống kê
- ✅ Xem danh sách sinh viên trong lớp
- ✅ Tạo và quản lý lịch tư vấn
- ✅ Phản hồi phiếu tư vấn từ sinh viên
- ✅ Xem thông báo và đánh giá từ sinh viên
- ✅ Thống kê lớp với biểu đồ tương tác
- ✅ **Xuất báo cáo đẹp theo mẫu trường đại học**

## 6. Giao diện mới

### Theme màu sắc:
- **Primary Blue**: #1e3a8a (Xanh chính)
- **Secondary Blue**: #3b82f6 (Xanh phụ)
- **Accent Gold**: #f59e0b (Vàng nhấn)
- **Success Green**: #10b981 (Xanh thành công)
- **Warning Orange**: #f97316 (Cam cảnh báo)

### Components:
- **Cards**: Bo góc, shadow, hover effects
- **Buttons**: Gradient, hover animations
- **Tables**: Striped, hover, responsive
- **Forms**: Modern input styling
- **Charts**: Interactive với tooltips
- **Navigation**: Responsive với icons

### Print Styles:
- Header trường đại học chuẩn
- Bảng dữ liệu tối ưu cho in
- Phần chữ ký và ngày tháng
- CSS print media queries

## 7. Cấu trúc files mới

```
static/
├── css/
│   └── education-theme.css    # Theme CSS chính
└── images/
    └── university-logo.png    # Logo trường (placeholder)

templates/
├── base.html                  # Base template với Bootstrap 5
├── auth/login.html           # Trang đăng nhập đẹp
├── sinhvien/
│   ├── dashboard.html        # Dashboard sinh viên
│   └── thong_ke.html        # Thống kê với biểu đồ
├── covan/
│   ├── dashboard.html        # Dashboard cố vấn  
│   └── bao_cao.html         # Báo cáo in đẹp
└── ...
```

## 8. Lưu ý

- Thay thế `static/images/university-logo.png` bằng logo thật của trường
- Cập nhật tên trường trong templates nếu cần
- Đảm bảo MySQL service đang chạy
- Sử dụng `python manage.py collectstatic` để load CSS
- Giao diện tối ưu cho màn hình từ mobile đến desktop

## 9. Screenshots

Hệ thống hiện có giao diện chuyên nghiệp với:
- 🎨 Trang đăng nhập gradient đẹp mắt
- 📊 Dashboard với cards thống kê trực quan  
- 📈 Biểu đồ tương tác với Chart.js
- 🖨️ Trang in báo cáo theo mẫu trường đại học
- 📱 Responsive design cho mọi thiết bị