# Đánh giá kết quả Bài tập số 2 – API Authentication

Đánh giá dựa trên đề bài **02_API_Authentication.md** và các evidence trong **evidences/02**.

---

## 1. Tổng quan

| Phần | Yêu cầu | Evidence có | Đánh giá |
|------|--------|-------------|----------|
| 1.1 | POST /api/login (token + user / 401) | POST:api:login.png | ✅ Đạt |
| 1.2 | GET /api/me (token → user, thiếu/sai → 401) | GET:api:me_with_token.png, GET:api:me-401.png | ✅ Đạt |
| 2.1 | PUT/DELETE cần token; chỉ sửa/xóa chính mình (403 nếu id khác) | PUT:api:users:int_id-*.png, DELETE:api:users:int_id*.png | ✅ Đạt |
| 2.2 | (Tùy chọn) Bảo vệ POST /api/users | Thể hiện trong code | ✅ Đạt |
| 3.1 | POST /api/logout thu hồi token | POST:api:logout.png | ✅ Đạt |

**Kết luận:** Đã hoàn thành đầy đủ các phần bắt buộc và phần tùy chọn (2.2), có evidence tương ứng cho login, /api/me, PUT/DELETE (thành công, 401, 403) và logout.

---

## 2. Chi tiết đánh giá theo từng phần

### Phần 1 – Đăng nhập API và phát token

- **1.1 POST /api/login:** Route nhận body JSON email/password, tìm user theo email, so sánh password. Đúng: tạo token bằng `uuid.uuid4().hex`, lưu vào `User.token` (database), trả về `{"token": "...", "user": {id, name, email}}` status 200. Sai email hoặc sai password đều trả 401; bài làm tách message "Invalid email" / "Invalid password" — đề gợi ý chung "Invalid email or password" nhưng tách hai trường hợp vẫn chấp nhận được. Evidence: POST:api:login.png → **Đạt.**

- **1.2 GET /api/me:** Hàm `get_user_from_token()` đọc header `Authorization`, bỏ tiền tố "Bearer ", tra `User.query.filter(User.token == token).first()`. Token hợp lệ thì trả thông tin user (id, name, email), không có password; thiếu/sai token trả `{"error": "Unauthorized"}` 401. Evidence: GET:api:me_with_token.png, GET:api:me-401.png → **Đạt.**

### Phần 2 – Bảo vệ một số route có sẵn

- **2.1 PUT và DELETE /api/users/<id>:** Trong `call_api_users_with_id`: kiểm tra token trước, không có user thì 401 "Unauthorized"; có user nhưng `user.id != id` thì 403 "Forbidden"; chỉ khi token đúng và id trùng mới thực hiện GET/PUT/DELETE. Đúng yêu cầu bảo vệ PUT và DELETE, và chỉ cho sửa/xóa chính mình. Evidence: PUT/DELETE thành công (có header token), PUT/DELETE forbidden (id khác), PUT/DELETE wrong_or_lack (token sai/thiếu) → **Đạt.**

  **Lưu ý:** GET /api/users/<id> cũng được bảo vệ (chỉ trả về user khi id = user đăng nhập). Đề bài chỉ yêu cầu bảo vệ PUT và DELETE; đây là mở rộng hợp lý (chỉ xem được chính mình).

- **2.2 POST /api/users (tùy chọn):** Đã triển khai: chỉ khi có token hợp lệ mới cho gọi `create_user()`, không token thì 401. → **Đạt.**

### Phần 3 – Đăng xuất API

- **3.1 POST /api/logout:** Đọc token từ header, nếu token hợp lệ thì gán `user.token = None` và commit, trả `{"message": "Logged out"}` 200. Token không hợp lệ trả 401 (đã chọn rõ trong code). Evidence: POST:api:logout.png → **Đạt.**

---

## 3. Điểm mạnh

- Token lưu trong database (cột `User.token`) thay vì in-memory dict — sau khi restart server token vẫn dùng được (trừ khi logout), phù hợp thực tế hơn.
- Đủ evidence cho luồng chính: login → /api/me (có token / không token) → PUT/DELETE (thành công, 401, 403) → logout.
- Helper `get_user_from_token()` dùng chung cho /api/me, PUT/DELETE, POST /api/users, logout; code gọn, dễ bảo trì.
- Phân biệt rõ 401 (Unauthorized) và 403 (Forbidden) đúng chuẩn HTTP.

---

## 4. Gợi ý cải thiện (không trừ điểm)

- **Login message:** Có thể thống nhất một message cho cả sai email và sai password: `{"error": "Invalid email or password"}` để không lộ thông tin “email có tồn tại hay không” (bảo mật tốt hơn).
- **PUT update_user – trùng name:** Hiện tại `User.query.filter(User.name == name).first()` có thể trùng chính user đang sửa (ví dụ giữ nguyên tên). Nên loại trừ user hiện tại: `User.query.filter(User.name == name, User.id != found_id.id).first()` để tránh báo "name existed" khi không đổi tên.
- **GET /api/users/<id>:** Nếu muốn đúng yêu cầu đề “chỉ bảo vệ PUT và DELETE”, có thể tách: GET /api/users/<id> không cần token (ai cũng xem được theo id), còn PUT/DELETE vẫn bắt token và kiểm tra id. Hiện tại cách làm “chỉ xem được chính mình” cũng chấp nhận được như mở rộng.

---

## 5. Kết luận

- **Hoàn thành:** Đủ Phần 1 (login, /api/me), Phần 2 (bảo vệ PUT/DELETE, tùy chọn POST /api/users), Phần 3 (logout).
- **Evidence:** Đủ và đúng với từng endpoint (thành công, 401, 403).
- **Đánh giá:** **Đạt** — bài tập số 2 (API Authentication) hoàn thành tốt.

Chúc em tiếp tục làm tốt các bài tiếp theo.
