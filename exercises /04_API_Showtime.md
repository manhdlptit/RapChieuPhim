# Đề bài: API cho Suất chiếu (Showtime)

Sau khi đã có API User, xác thực và API Phim (bài 1, 2, 3), bài này giúp em thêm **Suất chiếu (Showtime)** — một tài nguyên gắn với **Phim** (quan hệ một-nhiều: một phim có nhiều suất chiếu). Em sẽ luyện: model có **foreign key**, API cho resource con (nested hoặc độc lập), và tái sử dụng token để bảo vệ thao tác tạo/sửa/xóa.

**Lưu ý:** Tên class, tên route API, tên biến và key trong JSON **bắt buộc dùng tiếng Anh** (ví dụ: `Showtime`, `/api/showtimes`, `movie_id`, `start_time`).

---

## Kiến thức cần dùng

- **Foreign key (SQLAlchemy):** Model `Showtime` có cột `movie_id` tham chiếu đến `Movie.id`; dùng `db.ForeignKey("list_movies.id")` (hoặc tên bảng của model Movie) và quan hệ `relationship` nếu cần.
- **Nested resource:** URL dạng `/api/movies/<int:movie_id>/showtimes` để lấy danh sách suất chiếu của một phim.
- **Resource độc lập:** URL `/api/showtimes` và `/api/showtimes/<id>` cho CRUD đầy đủ (tùy cách thiết kế).
- **Token (bài 2):** Dùng lại `get_user_from_token()` để bảo vệ POST/PUT/DELETE nếu chỉ user đăng nhập mới được quản lý suất chiếu.

---

## Phần 1 – Model Showtime và quan hệ với Movie

### Bài 1.1 – Model Showtime

- Tạo model **`Showtime`** với các trường (tên cột tiếng Anh):
  - **`id`**: Integer, primary key, tự tăng.
  - **`movie_id`**: Integer, **foreign key** tham chiếu đến bảng phim (ví dụ `list_movies.id` hoặc bảng tương ứng của model Movie). Không NULL.
  - **`start_time`**: DateTime (thời điểm bắt đầu suất chiếu). Có thể dùng `db.DateTime` trong SQLAlchemy. Không NULL.
  - **`room`**: String (tên phòng chiếu, ví dụ "Phòng 1", "Room A"). Có thể NULL hoặc có giá trị mặc định.
- Chạy (hoặc cập nhật) `db.create_all()` để tạo bảng.
- **Gợi ý:** Đặt model trong cùng file model hiện có (ví dụ `models.py` hoặc `blueprints/model.py`). Đảm bảo model `Movie` (hoặc `Movies`) đã tồn tại trước khi tạo bảng Showtime.

---

### Bài 1.2 – Danh sách suất chiếu của một phim (GET nested)

- Tạo route **`GET /api/movies/<int:movie_id>/showtimes`**.
- Lấy tất cả suất chiếu có `movie_id` trùng với `movie_id` trong URL.
- Trả về JSON dạng **list**. Mỗi phần tử gồm: `id`, `movie_id`, `start_time`, `room` (có thể bỏ qua field NULL hoặc trả `null` — thống nhất với bài 3).
- **Nếu phim không tồn tại:** Trả về `{"error": "Movie not found"}` và **status 404**.
- **Gợi ý:** Trước tiên kiểm tra `Movie` có tồn tại với `id = movie_id` không; nếu không thì 404. Sau đó `Showtime.query.filter_by(movie_id=movie_id).order_by(Showtime.start_time).all()`.

---

### Bài 1.3 – Lấy một suất chiếu theo id (GET toàn cục)

- Tạo route **`GET /api/showtimes/<int:id>`**.
- Nếu có suất chiếu với `id` đó: trả về JSON gồm `id`, `movie_id`, `start_time`, `room`.
- Nếu không có: trả về JSON `{"error": "Showtime not found"}` và **status 404**.

---

## Phần 2 – API tạo và cập nhật (POST, PUT)

### Bài 2.1 – Tạo suất chiếu cho một phim

- Tạo route **`POST /api/movies/<int:movie_id>/showtimes`** (nested) **hoặc** **`POST /api/showtimes`** với body có `movie_id`.
  - **Nếu dùng nested:** URL đã có `movie_id`, body JSON: `{"start_time": "...", "room": "..."}`. Format `start_time`: em chọn (ví dụ ISO 8601 `"2026-03-15T19:00:00"` hoặc `"2026-03-15 19:00:00"`), server parse thành datetime.
  - **Nếu dùng `/api/showtimes`:** Body JSON: `{"movie_id": 1, "start_time": "...", "room": "..."}`.
- **Validation:** `movie_id` (nếu trong body) và `start_time` bắt buộc. Phim phải tồn tại. `start_time` phải là thời điểm hợp lệ. `room` tùy chọn.
- **Nếu hợp lệ:** Tạo bản ghi Showtime, `db.session.add` + `commit`, trả về thông tin suất chiếu vừa tạo và **status 201**.
- **Nếu lỗi (phim không tồn tại, thiếu start_time, format sai):** Trả về JSON `{"error": "..."}` (message tiếng Anh) và **status 400** hoặc **404** tùy trường hợp.
- **(Tùy chọn)** Chỉ cho phép gọi khi đã gửi token hợp lệ; nếu không: 401.

---

### Bài 2.2 – Cập nhật suất chiếu

- Tạo route **`PUT /api/showtimes/<int:id>`**.
- Body JSON: có thể gửi một hoặc nhiều field: `{"start_time": "...", "room": "..."}` (không gửi `movie_id` để đơn giản, hoặc cho phép đổi phim tùy em). Chỉ cập nhật những field client gửi.
- Nếu suất chiếu tồn tại và dữ liệu hợp lệ: cập nhật, commit, trả về thông tin suất chiếu sau khi cập nhật và **status 200**.
- Nếu không tồn tại: **404** và `{"error": "Showtime not found"}`.
- Nếu validation lỗi (ví dụ start_time không hợp lệ): **400** và message lỗi (tiếng Anh).
- **(Tùy chọn)** Chỉ cho phép khi có token hợp lệ; nếu không: 401.

---

## Phần 3 – Xóa (DELETE)

### Bài 3.1 – Xóa suất chiếu qua API

- Tạo route **`DELETE /api/showtimes/<int:id>`**.
- Nếu suất chiếu tồn tại: xóa, commit, trả về JSON `{"message": "Showtime deleted"}` và **status 200**.
- Nếu không tồn tại: **404** và `{"error": "Showtime not found"}`.
- **(Tùy chọn)** Chỉ cho phép khi có token hợp lệ; nếu không: 401.

---

## Phần 4 – Tự kiểm tra (không bắt buộc nộp)

- Dùng Postman (hoặc curl):
  - Tạo ít nhất một phim (POST /api/movies) nếu chưa có.
  - Gọi `GET /api/movies/<movie_id>/showtimes` khi chưa có suất chiếu → list rỗng `[]`; khi phim không tồn tại → 404.
  - Tạo suất chiếu bằng POST (nested hoặc POST /api/showtimes); kiểm tra `start_time` format (ISO hoặc em chọn).
  - Gọi `GET /api/movies/<movie_id>/showtimes` và `GET /api/showtimes/<id>` để kiểm tra dữ liệu.
  - Thử PUT (cập nhật một phần), DELETE; thử id không tồn tại → 404, validation lỗi → 400.
- Chụp màn hình (evidence) và lưu vào thư mục **evidences/04** (tên file gợi ý: `GET:api:movies:int_id:showtimes.png`, `POST:api:movies:int_id:showtimes.png`, `GET:api:showtimes:int_id.png`, `PUT:api:showtimes:int_id.png`, `DELETE:api:showtimes:int_id.png`, …).

---

## Lưu ý

- Giữ nguyên model **User**, **Movie** và toàn bộ API User, API Movies (bài 1, 2, 3). Chỉ **thêm** model `Showtime` và các route **`/api/movies/<id>/showtimes`**, **`/api/showtimes`**, **`/api/showtimes/<id>`**.
- Tên class, route, key trong request/response JSON (như `movie_id`, `start_time`, `room`, `error`, `message`) **phải dùng tiếng Anh**.
- **Format datetime:** Thống nhất một format cho `start_time` (ví dụ ISO 8601) khi nhận từ client và khi trả về JSON (có thể dùng `datetime.isoformat()` hoặc string theo quy ước).

Chúc em làm bài tốt!
