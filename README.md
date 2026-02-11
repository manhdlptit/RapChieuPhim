🛠 1. Yêu cầu hệ thống & Tiện ích (VS Code)
Để dự án hoạt động mượt mà, hãy cài đặt các Extension sau trên VS Code:

Python Bundle: Python, Pylance, Python Debugger (Microsoft).

Jinja: Jinja (wholroyd) - Hỗ trợ định dạng file HTML.

Database: SQLite Viewer (Florian Klampfer) - Để xem dữ liệu file .db.

📦 2. Cài đặt và Thiết lập
Mở Terminal của bạn (hoặc Terminal tích hợp trong VS Code) và làm theo các bước sau:

Bước 1: Tải mã nguồn về máy

Bash

git clone <link-github-cua-ban>
cd <ten-thu-muc-du-an>

Bước 2: Khởi tạo môi trường ảo (Virtual Environment)
Việc này giúp tránh xung đột thư viện giữa các dự án khác nhau.

Trên macOS / Linux:

Bash

python3 -m venv venv
source venv/bin/activate

Trên Windows:

PowerShell

python -m venv venv
.\venv\Scripts\activate

Bước 3: Cài đặt các thư viện cần thiết

Bash

pip install Flask flask-sqlalchemy

🏃 3. Khởi chạy ứng dụng

Sau khi cài đặt xong, bạn có thể chạy ứng dụng bằng lệnh:

Bash

python main.py

Hoặc dùng giao diện VS Code:

Mở file main.py.

Nhấn biểu tượng Play ở góc trên bên phải.

🌐 4. Cách sử dụng

Khi terminal hiển thị: Running on http://127.0.0.1:8000

Giữ phím Command (macOS) hoặc Ctrl (Windows) và Click chuột trái vào đường link đó.

Trình duyệt sẽ mở ứng dụng. Chúc bạn trải nghiệm vui vẻ!

📂 5. Cấu trúc thư mục dự án

Plaintext

├── static/          # Chứa CSS, hình ảnh, JavaScript

├── templates/       # Các file giao diện HTML (Jinja2)

├── main.py          # File khởi chạy ứng dụng chính

├── instance/        # Chứa cơ sở dữ liệu SQLite (.db)

└── README.md        # Tài liệu hướng dẫn này

📝 Lưu ý quan trọng

Nếu lệnh python không hoạt động trên Mac/Linux, hãy dùng python3.

Nếu lệnh pip không hoạt động, hãy dùng pip3.
