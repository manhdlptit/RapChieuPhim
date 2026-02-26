# Đánh giá kết quả Bài tập số 3 – API cho tài nguyên Phim (Movies)

Đánh giá dựa trên đề bài **03_API_Phim.md** và các evidence trong **evidences/03**.

---

## 1. Tổng quan

| Phần | Yêu cầu | Evidence có | Đánh giá |
|------|--------|-------------|----------|
| 1.1 | Model Movie (id, title, duration_minutes, description) | Thể hiện trong code | ✅ Đạt |
| 1.2 | GET /api/movies (danh sách JSON) | GET:api:movies_when_have_movie.png, GET:api:movies_when_have_not_movie.png | ✅ Đạt |
| 1.3 | GET /api/movies/<id> (một phim hoặc 404) | Thể hiện qua PUT/DELETE với id | ✅ Đạt |
| 2.1 | POST /api/movies (validation, 201/400) | POST:api:movies.png, POST:api:movies_but_*.png | ✅ Đạt |
| 2.2 | PUT /api/movies/<id> (cập nhật một phần, 200/404/400) | PUT:api:movies_*.png (4 ảnh) | ✅ Đạt |
| 3.1 | DELETE /api/movies/<id> (200/404) | DELETE:api:movie.png, DELETE:api:movie_if_not_id.png | ✅ Đạt |

**Kết luận:** Đã hoàn thành đầy đủ các phần theo đề bài; có evidence cho GET (list rỗng/có dữ liệu), POST (thành công, lỗi validation/trùng), PUT (thành công, cập nhật một phần, lỗi, không tồn tại), DELETE (thành công, 404).

---

## 2. Chi tiết đánh giá theo từng phần

### Phần 1 – Model và API đọc (GET)

- **1.1 Model:** Class **`Movies`** (số nhiều) với các cột `id`, `title`, `duration_minutes`, `description`; `title` có `nullable=False`; bảng `list_movies` qua `__tablename__`. Đề gợi ý tên class `Movie` (số ít) — dùng `Movies` vẫn đúng quy định “tên class tiếng Anh”. `db.create_all()` được gọi trong `if __name__ == "__main__"` → **Đạt.**

- **1.2 GET /api/movies:** Hàm `list_movies()` dùng `Movies.query.order_by(Movies.id).all()`, trả về list JSON gồm `id`, `title`, `duration_minutes`, `description`. Route `/api/movies` GET được gắn với `list_movies()`; hiện tại yêu cầu token (tùy chọn theo đề). Evidence: list khi chưa có phim và khi đã có phim → **Đạt.**

- **1.3 GET /api/movies/<id>:** Hàm `list_movies_with_id(id)` dùng `db.session.get(Movies, id)`; có thì trả JSON đủ 4 field, không có thì `{"error": "Movie not found"}` và 404 → **Đạt.**

### Phần 2 – API tạo và cập nhật (POST, PUT)

- **2.1 POST /api/movies:** Đọc body bằng `request.get_json()`. Validation: `title` bắt buộc (None hoặc chuỗi rỗng sau strip → 400 "Title is required"); `duration_minutes` nếu có phải không âm (số âm → 400). Có thêm kiểm tra phim trùng (cùng title + duration_minutes + description) và trả 400 — hợp lý. Tạo bản ghi, commit, trả thông tin phim (trong object `movie`). Evidence: tạo mới thành công, duration âm, phim đã tồn tại → **Đạt.**

  **Gợi ý:** Đề yêu cầu trả **status 201** khi tạo thành công; hiện tại response không khai báo status nên mặc định 200. Nên thêm `, 201` vào `return jsonify(...)` khi tạo phim thành công.

- **2.2 PUT /api/movies/<id>:** `update_movie(id)` lấy phim theo id; không tồn tại → 404 "Movie not found". Đọc body, dùng `.get(field, found_id.field)` để chỉ cập nhật field client gửi. Validation: title không rỗng, duration_minutes không âm; lỗi → 400. Trả về thông tin phim sau khi cập nhật, status 200. Evidence: cập nhật thành công, chỉ gửi title, title không hợp lệ, id không tồn tại → **Đạt.**

### Phần 3 – Xóa (DELETE)

- **3.1 DELETE /api/movies/<id>:** Có phim thì xóa, commit, trả `{"message": "Movie deleted"}` 200; không có thì 404 `{"error": "Movie not found"}`. Evidence: xóa thành công và id không tồn tại → **Đạt.**

### Bảo vệ bằng token (tùy chọn)

- Toàn bộ route `/api/movies` và `/api/movies/<id>` đều yêu cầu token (`get_user_from_token()`); không token trả 401. Đề bài nêu token là tùy chọn cho POST/PUT/DELETE; việc bảo vệ cả GET là mở rộng chấp nhận được → **Đạt.**

---

## 3. Điểm mạnh

- Đủ evidence cho nhiều tình huống: list rỗng/có dữ liệu, tạo thành công và lỗi (validation, trùng), PUT thành công/một phần/lỗi/404, DELETE thành công/404.
- Validation rõ: title bắt buộc, duration_minutes không âm; có kiểm tra trùng phim khi tạo.
- Tên class, route, key JSON đều dùng tiếng Anh đúng yêu cầu (`Movies`, `/api/movies`, `title`, `duration_minutes`, `description`, `error`, `message`).
- Cập nhật PUT đúng kiểu “partial update”: chỉ đổi các field client gửi.

---

## 4. Gợi ý cải thiện (không trừ điểm)

- **POST trả về 201:** Khi tạo phim thành công nên trả **status 201** (Created), ví dụ: `return jsonify({...}), 201`.
- **Tên class:** Đề gợi ý `Movie` (số ít); hiện dùng `Movies`. Nếu đổi sang `Movie` thì thống nhất với tên resource trong URL `/api/movies` (số nhiều cho collection là chuẩn REST).
- **Response POST:** Hiện trả `{"successfully": "...", "movie": {...}}`. Đề chỉ yêu cầu “trả về thông tin phim vừa tạo”; có thể trả trực tiếp object phim (và status 201) để đơn giản, client vẫn dùng được.

---

## 5. Kết luận

- **Hoàn thành:** Đủ Phần 1 (model Movie/Movies, GET list, GET by id), Phần 2 (POST, PUT), Phần 3 (DELETE); có bảo vệ bằng token cho toàn bộ API movies.
- **Evidence:** Đủ và phù hợp với từng nhóm endpoint (thành công và lỗi).
- **Đánh giá:** **Đạt** — bài tập số 3 (API cho tài nguyên Phim) hoàn thành tốt.

Chúc em tiếp tục làm tốt các bài tiếp theo.
