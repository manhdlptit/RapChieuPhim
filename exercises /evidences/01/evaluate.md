# Đánh giá kết quả Bài tập số 1 – API Flask

Đánh giá dựa trên đề bài **01_API_Flask.md** và các evidence trong **evidences/01**.

---

## 1. Tổng quan

| Phần | Yêu cầu | Evidence có | Đánh giá |
|------|--------|-------------|----------|
| 1.1 | GET /api/hello | api:hello.png | ✅ Đạt |
| 1.2 | GET /api/users | GET:api:users:.png | ✅ Đạt |
| 1.3 | GET /api/users/<id> | GET:api:users:int_id.png, GET:api:users:int_id_but_error_not_existed_id.png | ✅ Đạt |
| 2.1 | POST /api/users | POST:api:users_create_user.png, POST:api:users_create_user_but_existed.png | ✅ Đạt |
| 2.2 | GET /api/users/search | GET:api:users:search_*.png (3 ảnh) | ✅ Đạt |
| 3.1 | PUT /api/users/<id> | PUT:api:users:int_id.png, PUT:api:users:int_id_but_not_found_id.png, PUT:api:users:int_id_but_name_existed.png | ✅ Đạt |
| 3.2 | DELETE /api/users/<id> | DELETE:api:users:int_id.png, DELETE:api:users:int_id_but_id_not_found.png | ✅ Đạt |

**Kết luận:** Đã hoàn thành đầy đủ các phần theo đề bài và có evidence tương ứng cho từng endpoint (kể cả trường hợp thành công và lỗi).

---

## 2. Chi tiết đánh giá theo từng phần

### Phần 1 – API đơn giản

- **1.1 Hello API:** Có evidence Postman: GET `/api/hello` trả về 200 OK và `{"message": "Hello from API"}` → **Đạt.**
- **1.2 Danh sách user:** Code dùng `User.query.all()`, trả về list chỉ gồm `id`, `name`, `email` (không có password) → **Đạt.**
- **1.3 User theo id:** Có user thì trả về JSON user, không có thì 404 và `{"error": "User not found"}`; có evidence cho cả hai trường hợp → **Đạt.**

### Phần 2 – API nhận dữ liệu (POST)

- **2.1 Tạo user:** Đọc body bằng `request.get_json()`, kiểm tra email/name trùng và trả 400, tạo user và trả 201 với thông tin user (không password). Có evidence tạo mới và trường hợp email/name đã tồn tại → **Đạt.**
- **2.2 Tìm user theo email:** Route `GET /api/users/search`, dùng `request.args.get("email")`. Có evidence: không truyền email, có email và tìm thấy, có email nhưng không tìm thấy. Đề cho phép chọn 400 hoặc 404 khi lỗi; bài làm dùng 404 khi không nhập email và 400 khi không tìm thấy email → **Đạt.**

### Phần 3 – Cập nhật và xóa (PUT, DELETE)

- **3.1 Cập nhật tên:** PUT `/api/users/<int:id>`, cập nhật `name`, trả 200 khi thành công và 404 khi không tìm thấy. Có thêm kiểm tra **tên trùng** (name đã tồn tại) và trả lỗi — vượt yêu cầu đề bài, hợp lý với nghiệp vụ → **Đạt.**
- **3.2 Xóa user:** DELETE đúng id thì xóa và trả 200 với `{"message": "User deleted"}`, id không tồn tại thì 404 và `{"error": "User not found"}`. Có đủ evidence → **Đạt.**

---

## 3. Điểm mạnh

- Đủ evidence cho **tất cả** endpoint và cho cả **trường hợp lỗi** (404, 400, name/email trùng), thể hiện đã tự kiểm tra kỹ (Phần 4).
- Code gọn: tách hàm phụ (`print_user`, `create_user`, `update_user`, …) rồi gọi trong route, dễ đọc.
- Không trả về `password` trong bất kỳ response JSON nào.
- Có xử lý ngoại lệ bằng `try/except` ở nhiều chỗ (có thể tối ưu sau: trả status code và message thống nhất).

---

## 4. Gợi ý cải thiện (không trừ điểm)

- **PUT khi name trùng:** Hiện trả về JSON lỗi nhưng chưa ghi rõ status code (ví dụ 400). Nên trả thêm status 400 để client phân biệt với 404.
- **GET /api/users/search:** Khi không truyền `email` dùng 404; đề cho phép 400 hoặc 404. Có thể ghi rõ trong comment hoặc tài liệu API: “404 = thiếu tham số email” để tránh nhầm với “user không tồn tại”.
- **Validation POST /api/users:** Đề yêu cầu “password không rỗng”; code đang kiểm tra “không null bất kỳ field nào” — đúng với ý đề. Có thể bổ sung kiểm tra độ dài tối thiểu password nếu muốn chặt hơn.

---

## 5. Kết luận

- **Hoàn thành:** Đủ các phần 1, 2, 3 theo đề bài 01_API_Flask.md.
- **Evidence:** Đủ và đúng với từng endpoint (thành công + lỗi).
- **Đánh giá:** **Đạt** — sẵn sàng chuyển sang Bài tập số 2 (API Authentication / bảo vệ API).

Chúc em tiếp tục làm tốt bài số 2.
