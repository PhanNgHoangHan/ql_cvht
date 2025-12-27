#!/bin/bash

# Chờ MySQL local khởi động
echo "Đang chờ MySQL local khởi động..."
while ! nc -z host.docker.internal 3307; do
  echo "Đang chờ MySQL local trên host.docker.internal:3307..."
  sleep 2
done
echo "MySQL local đã sẵn sàng!"

# Chạy migrations
echo "Chạy database migrations..."
python manage.py migrate

# Khởi tạo dữ liệu cơ bản
echo "Khởi tạo dữ liệu cơ bản..."
python docker-init-data.py

# Collect static files
echo "Thu thập static files..."
python manage.py collectstatic --noinput

# Chạy setup system nếu file tồn tại
if [ -f "setup_system.py" ]; then
    echo "Chạy setup system..."
    python setup_system.py
fi

# Khởi động Django server
echo "Khởi động Django server..."
python manage.py runserver 0.0.0.0:8000