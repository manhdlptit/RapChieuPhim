# Đề bài: Xác thực API (API Authentication)

Sau khi đã có các API CRUD cho User (bài 1), bài này giúp em thêm **đăng nhập qua API** và **bảo vệ** một số route — chỉ cho phép gọi khi client gửi kèm token hợp lệ.

---

## Kiến thức cần dùng

- **Header trong HTTP:** Client gửi token qua header, ví dụ: `Authorization: Bearer <token>`.
- **`request.headers.get("Authorization")`**: Đọc header từ request trong Flask.
- **Hàm decorator** hoặc **before_request**: Kiểm tra token trước khi vào route (hoặc dùng decorator cho từng route cần bảo vệ).
- **Token đơn giản:** Có thể dùng `uuid.uuid4()` hoặc chuỗi ngẫu nhiên, lưu vào bộ nhớ (dict) hoặc bảng trong database (tùy em chọn).

---

## Phần 1 – Đăng nhập API và phát token

### Bài 1.1 – Endpoint đăng nhập

- Tạo route **`POST /api/login`**.
- Body JSON: `{"email": "...", "password": "..."}`.
- Nếu email tồn tại và password đúng:
  - Tạo một **token** (chuỗi ngẫu nhiên, ví dụ `uuid.uuid4().hex`).
  - Lưu token gắn với user (trong dict in-memory: `token → user_id`, hoặc tạo model/bảng Token tùy em).
  - Trả về JSON: `{"token": "<token>", "user": {"id": ..., "name": ..., "email": ...}}` và **status 200**.
- Nếu email hoặc password sai: trả về `{"error": "Invalid email or password"}` và **status 401**.

**Gợi ý:**  
- Đọc `request.get_json()`, lấy email/password.  
- `User.query.filter_by(email=email).first()`, so sánh password.  
- Lưu token: ví dụ `tokens = {}` ở ngoài route, mỗi lần login `tokens[token] = user.id`.

---

### Bài 1.2 – Endpoint “user hiện tại” (chỉ khi đã đăng nhập)

- Tạo route **`GET /api/me`**.
- Client gửi kèm token trong header: **`Authorization: Bearer <token>`**.
- Nếu token hợp lệ: trả về thông tin user (id, name, email, không password) và **status 200**.
- Nếu thiếu token hoặc token không hợp lệ: trả về `{"error": "Unauthorized"}` và **status 401**.

**Gợi ý:**  
- Hàm helper `get_user_from_token()`: đọc `request.headers.get("Authorization")`, bỏ tiền tố `"Bearer "`, tra trong `tokens` (hoặc bảng Token) lấy `user_id`, rồi `User.query.get(user_id)`.  
- Trong route `GET /api/me`, gọi helper đó; nếu không có user thì trả 401.

---

## Phần 2 – Bảo vệ một số route có sẵn

Em đã có các route: `GET/POST /api/users`, `GET/PUT/DELETE /api/users/<id>`, `GET /api/users/search`. Trong bài này chỉ cần **bảo vệ** một phần (đủ để thể hiện cách làm).

### Bài 2.1 – Bảo vệ PUT và DELETE

- **PUT /api/users/<int:id>** và **DELETE /api/users/<int:id>** chỉ được gọi khi request có header **`Authorization: Bearer <token>`** và token hợp lệ.
- Nếu thiếu token hoặc token sai: trả về `{"error": "Unauthorized"}` và **401** (không thực hiện cập nhật/xóa).
- Nếu token đúng nhưng user đăng nhập chỉ được sửa/xóa **chính mình**: chỉ cho PUT/DELETE khi `id` trong URL bằng `user_id` của token. Nếu id khác (sửa/xóa user khác): trả về `{"error": "Forbidden"}` và **403**.

**Gợi ý:**  
- Tạo decorator `@require_token` (hoặc hàm kiểm tra gọi ở đầu route).  
- Trong route PUT/DELETE: sau khi có user từ token, so sánh `user.id` với `id` trong URL; nếu khác thì 403.

---

### Bài 2.2 – (Tùy chọn) Bảo vệ POST /api/users

- Chỉ cho phép **tạo user mới** (POST /api/users) khi đã gửi token hợp lệ (tức “chỉ user đã đăng nhập mới được tạo user mới”).  
- Nếu chưa đăng nhập: 401.  
- Nếu em muốn giữ POST /api/users là “đăng ký công khai” thì có thể bỏ qua bài 2.2 và ghi rõ trong bài làm.

---

## Phần 3 – Đăng xuất (logout) API

### Bài 3.1 – Thu hồi token

- Tạo route **`POST /api/logout`**.
- Client gửi header **`Authorization: Bearer <token>`**.
- Nếu token hợp lệ: xóa token khỏi bộ lưu trữ (dict hoặc xóa bản ghi trong bảng Token), trả về `{"message": "Logged out"}` và **status 200**.
- Nếu token không hợp lệ hoặc đã hết hạn: vẫn có thể trả 200 và `{"message": "Logged out"}` (để client có thể “quên” token), hoặc trả 401 — em chọn một và ghi rõ.

---

## Phần 4 – Tự kiểm tra (không bắt buộc nộp)

- Dùng Postman (hoặc curl):
  - Gọi `POST /api/login` với email/password đúng → lấy `token` trong response.
  - Gọi `GET /api/me` với header `Authorization: Bearer <token>` → kiểm tra trả về đúng user.
  - Gọi PUT/DELETE với token → chỉ thành công khi id trùng user đăng nhập; gọi với token sai hoặc thiếu → 401; gọi với id user khác → 403.
  - Gọi `POST /api/logout` với token → sau đó gọi lại `GET /api/me` với token đó → 401.
- Chụp màn hình (evidence) các request/response và lưu vào thư mục **evidences/02** (tên file gợi ý: `POST:api:login.png`, `GET:api:me_with_token.png`, …).

---

## Lưu ý

- Token có thể lưu in-memory (dict). Khi restart server thì mọi token cũ sẽ không còn — chấp nhận được cho bài tập. Nếu muốn, em có thể mở rộng: lưu token vào bảng trong database.
- Giữ nguyên model **User** và các route API bài 1; chỉ **thêm** route login/logout/me và **thêm** bước kiểm tra token cho PUT/DELETE (và tùy chọn POST /api/users).
- Khi trả về thông tin user, **không** đưa `password` vào JSON.

Chúc em làm bài tốt!
