# Đề bài: API cho tài nguyên Phim (Movies)

Sau khi đã có API User và xác thực (bài 1, 2), bài này giúp em thêm **một tài nguyên mới** — **Phim** — với model trong database và các endpoint REST API. Như vậy em sẽ luyện: tạo model mới, CRUD API cho resource thứ hai, và áp dụng lại token cho các thao tác cần bảo vệ.

**Lưu ý:** Tên class, tên route API, tên biến và key trong JSON **bắt buộc dùng tiếng Anh** (ví dụ: `Movie`, `/api/movies`, `title`, `duration_minutes`).

---

## Kiến thức cần dùng

- **SQLAlchemy model mới:** Định nghĩa class `Movie`, các cột và `db.create_all()` để tạo bảng.
- **REST API cho resource:** Quy ước URL `/api/movies` cho collection, `/api/movies/<id>` cho từng bản ghi.
- **Request body & validation:** Đọc JSON từ `request.get_json()`, kiểm tra bắt buộc (ví dụ: title không rỗng).
- **Token (bài 2):** Dùng lại `get_user_from_token()` để bảo vệ POST/PUT/DELETE nếu em muốn chỉ user đăng nhập mới được thêm/sửa/xóa phim.

---

## Phần 1 – Model và API đọc (GET)

### Bài 1.1 – Model Movie

- Tạo model **`Movie`** với các trường (tên cột tiếng Anh):
  - **`id`**: Integer, primary key, tự tăng.
  - **`title`**: String (tên phim), không để trống.
  - **`duration_minutes`**: Integer (thời lượng phút), có thể cho phép NULL nếu chưa có.
  - **`description`**: Text hoặc String dài (mô tả), có thể NULL.
- Chạy (hoặc cập nhật) `db.create_all()` để tạo bảng trong database.
- **Gợi ý:** Đặt model trong cùng file `main.py` (hoặc tách file models nếu đã quen). Tên bảng có thể để mặc định (snake_case của tên class) hoặc chỉ định `__tablename__`.

---

### Bài 1.2 – Danh sách phim (chỉ đọc)

- Tạo route **`GET /api/movies`**.
- Lấy tất cả phim từ bảng `Movie`, trả về JSON dạng **list**.
- Mỗi phần tử gồm: `id`, `title`, `duration_minutes`, `description` (có thể bỏ qua field NULL khi trả về, hoặc trả về `null` — em chọn một và thống nhất).
- **Gợi ý:** `Movie.query.all()`, tạo list dict rồi `jsonify(list đó)`. Có thể dùng `.order_by(Movie.id)` hoặc `.order_by(Movie.title)` để thứ tự ổn định.

---

### Bài 1.3 – Lấy một phim theo id

- Tạo route **`GET /api/movies/<int:id>`**.
- Nếu có phim với `id` đó: trả về JSON gồm `id`, `title`, `duration_minutes`, `description`.
- Nếu không có: trả về JSON `{"error": "Movie not found"}` và **status code 404**.

---

## Phần 2 – API tạo và cập nhật (POST, PUT)

### Bài 2.1 – Tạo phim qua API

- Tạo route **`POST /api/movies`**.
- Client gửi body JSON, ví dụ: `{"title": "...", "duration_minutes": 120, "description": "..."}`.
- **Validation:** `title` bắt buộc (không rỗng). `duration_minutes` nếu có phải là số dương (hoặc bỏ qua nếu không gửi). `description` tùy chọn.
- **Nếu hợp lệ:** Tạo bản ghi phim, `db.session.add` + `commit`, trả về thông tin phim vừa tạo và **status 201**.
- **Nếu lỗi (ví dụ thiếu title):** Trả về JSON `{"error": "Title is required"}` (hoặc message tương ứng, bằng tiếng Anh) và **status 400**.
- **(Tùy chọn)** Chỉ cho phép gọi khi đã gửi token hợp lệ (giống bài 2). Nếu không gửi token: 401.

---

### Bài 2.2 – Cập nhật phim

- Tạo route **`PUT /api/movies/<int:id>`**.
- Body JSON: có thể gửi một hoặc nhiều field: `{"title": "New title", "duration_minutes": 100, "description": "..."}`. Chỉ cập nhật những field client gửi lên (không gửi thì giữ nguyên).
- Nếu phim tồn tại và dữ liệu hợp lệ: cập nhật, commit, trả về thông tin phim sau khi cập nhật và **status 200**.
- Nếu không tồn tại: trả về **404** và `{"error": "Movie not found"}`.
- Nếu validation lỗi (ví dụ title rỗng): trả **400** và message lỗi (tiếng Anh).
- **(Tùy chọn)** Chỉ cho phép khi có token hợp lệ; nếu không: 401.

---

## Phần 3 – Xóa (DELETE)

### Bài 3.1 – Xóa phim qua API

- Tạo route **`DELETE /api/movies/<int:id>`**.
- Nếu phim tồn tại: xóa phim, commit, trả về JSON `{"message": "Movie deleted"}` và **status 200**.
- Nếu không tồn tại: trả về **404** và `{"error": "Movie not found"}`.
- **(Tùy chọn)** Chỉ cho phép khi có token hợp lệ; nếu không: 401.

---

## Phần 4 – Tự kiểm tra (không bắt buộc nộp)

- Dùng Postman (hoặc curl):
  - Gọi `GET /api/movies` khi chưa có phim → list rỗng `[]`.
  - Tạo vài phim bằng `POST /api/movies` (với hoặc không token nếu em đã bảo vệ).
  - Gọi `GET /api/movies` và `GET /api/movies/<id>` để kiểm tra dữ liệu.
  - Thử PUT (cập nhật một phần field), DELETE; thử id không tồn tại → 404, thiếu title → 400.
- Chụp màn hình (evidence) và lưu vào thư mục **evidences/03** (tên file gợi ý: `GET:api:movies.png`, `POST:api:movies.png`, `PUT:api:movies:int_id.png`, `DELETE:api:movies:int_id.png`, …).

---

## Lưu ý

- Có thể viết tất cả route trong **`main.py`** (hoặc tách blueprint cho `/api/movies` nếu đã học).
- Giữ nguyên model **User** và toàn bộ API User (bài 1, 2). Chỉ **thêm** model `Movie` và các route **`/api/movies`**.
- Tên class, tên route, key trong request/response JSON (như `title`, `description`, `error`, `message`) **phải dùng tiếng Anh**.
- Nếu sau này em muốn thêm **Suất chiếu** (Showtime) gắn với phim, có thể mở rộng: model `Showtime` có `movie_id` (foreign key) và endpoint `GET /api/movies/<id>/showtimes` — không bắt buộc trong bài 3.

Chúc em làm bài tốt!
