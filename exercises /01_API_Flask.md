# Đề bài: Viết API cho server Python (Flask)

Dự án của em đã có trang web với đăng ký, đăng nhập và model `User` trong database. Phần bài tập này giúp em bước đầu viết **API** — tức là các đường dẫn (route) **trả về dữ liệu JSON** thay vì trang HTML, để sau này có thể dùng cho app mobile hoặc frontend tách riêng.

---

## Kiến thức cần dùng

- **`jsonify()`**: Trả về JSON cho client (Flask đã có sẵn).
- **`request.get_json()`** hoặc **`request.json`**: Đọc dữ liệu JSON mà client gửi lên trong body (thường dùng cho POST, PUT).
- **`request.args.get("tên_tham_số")`**: Lấy tham số từ URL dạng `?email=abc@gmail.com`.
- **Status code**: Tham số thứ hai của `jsonify(..., 404)` hoặc `jsonify(..., 201)` để báo trạng thái HTTP.

---

## Phần 1 – API đơn giản (trả về JSON)

### Bài 1.1 – Endpoint "hello API"

- Tạo route **`GET /api/hello`**.
- Trả về JSON: `{"message": "Hello from API"}`.
- **Gợi ý:** Dùng `jsonify()` từ Flask.

---

### Bài 1.2 – Danh sách user (chỉ đọc)

- Tạo route **`GET /api/users`**.
- Lấy tất cả user từ bảng `User`, trả về JSON dạng list.
- Mỗi phần tử trong list gồm: `id`, `name`, `email` — **không** trả về `password`.
- **Gợi ý:** `User.query.all()`, tạo list dict rồi `jsonify(list đó)`.

---

### Bài 1.3 – Lấy một user theo id

- Tạo route **`GET /api/users/<int:id>`**.
- Nếu có user với `id` đó: trả về JSON gồm `id`, `name`, `email` (không có password).
- Nếu không có: trả về JSON `{"error": "User not found"}` và **status code 404**.
- **Gợi ý:** `User.query.get(id)` hoặc `User.query.filter_by(id=id).first()`, và `jsonify(..., 404)`.

---

## Phần 2 – API nhận dữ liệu (POST)

### Bài 2.1 – Tạo user qua API

- Tạo route **`POST /api/users`**.
- Client gửi body JSON, ví dụ: `{"email": "...", "name": "...", "password": "..."}`.
- Server đọc bằng **`request.get_json()`** (hoặc `request.json`).
- Kiểm tra: email/name chưa tồn tại, password không rỗng.
- **Nếu hợp lệ:** Tạo user, `db.session.add` + `commit`, trả về thông tin user (không có password) và **status 201**.
- **Nếu email hoặc name trùng:** Trả về JSON `{"error": "Email or name already exists"}` và **status 400**.

---

### Bài 2.2 – Tìm user theo email (query string)

- Tạo route **`GET /api/users/search`**.
- Nhận tham số `email` qua query string, ví dụ: `GET /api/users/search?email=abc@gmail.com`.
- **Gợi ý:** `request.args.get("email")`.
- Nếu có user: trả về JSON thông tin user (không password).
- Nếu không có hoặc không truyền `email`: trả về JSON thông tin lỗi và status **400** hoặc **404** (em chọn một và ghi rõ trong bài làm).

---

## Phần 3 – Cập nhật và xóa (PUT, DELETE)

### Bài 3.1 – Cập nhật tên user

- Tạo route **`PUT /api/users/<int:id>`**.
- Body JSON: `{"name": "Tên mới"}`.
- Nếu user tồn tại: cập nhật `name`, commit, trả về thông tin user sau khi cập nhật và **status 200**.
- Nếu không tồn tại: trả về **404** và `{"error": "User not found"}`.

---

### Bài 3.2 – Xóa user qua API

- Tạo route **`DELETE /api/users/<int:id>`**.
- Nếu user tồn tại: xóa user, commit, trả về JSON `{"message": "User deleted"}` và **status 200**.
- Nếu không tồn tại: trả về **404** và `{"error": "User not found"}`.

---

## Phần 4 – Tự kiểm tra (không bắt buộc nộp)

- Dùng trình duyệt (chỉ được GET) hoặc **Postman** / **curl** để gọi từng endpoint và kiểm tra JSON + status code.
- Thử các trường hợp lỗi: id không tồn tại, thiếu field, email trùng, v.v.

---

## Lưu ý

- Tất cả route API có thể viết trong cùng file **`main.py`** (hoặc tách file khác nếu đã học blueprint).
- Giữ nguyên model **`User`** và database hiện có.
- Khi trả về thông tin user, **không** đưa `password` vào JSON.

Chúc em làm bài tốt!
