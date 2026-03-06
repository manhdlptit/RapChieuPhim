# Đánh giá kết quả Bài tập số 4 – API cho Suất chiếu (Showtime)

Đánh giá dựa trên đề bài **04_API_Showtime.md** và các evidence trong **evidences/04**.

---

## 1. Tổng quan

| Phần | Yêu cầu | Evidence có | Đánh giá |
|------|--------|-------------|----------|
| 1.1 | Model Showtime (id, movie_id FK, start_time, room) | Thể hiện trong code | ✅ Đạt |
| 1.2 | GET /api/movies/\<movie_id\>/showtimes (list, 404 nếu phim không tồn tại) | GET:api:movies:\<movie_id\>:showtime_*.png (3 ảnh) | ✅ Đạt |
| 1.3 | GET /api/showtimes/\<id\> (một suất chiếu hoặc 404) | GET:api:movies:api:showtimes:\<id\>_*.png | ✅ Đạt |
| 2.1 | POST tạo suất chiếu (nested hoặc /api/showtimes), validation, 201 | POST:api:movies:\<movie_id\>:showtime_*.png (3 ảnh) | ✅ Đạt |
| 2.2 | PUT /api/showtimes/\<id\> (cập nhật một phần, 200/404/400) | PUT:api:movies:api:showtimes:\<id\>_*.png (2 ảnh) | ✅ Đạt |
| 3.1 | DELETE /api/showtimes/\<id\> (200/404) | DELETE:api:movies:api:showtimes:\<id\>_*.png (2 ảnh) | ✅ Đạt |

**Kết luận:** Đã hoàn thành đầy đủ các phần theo đề bài; có evidence cho GET nested (list rỗng, có dữ liệu, phim không tồn tại), POST (thành công, thiếu start_time, sai format), GET by id (tồn tại/không tồn tại), PUT (thành công, movie_id không tồn tại), DELETE (thành công, id không tồn tại).

---

## 2. Chi tiết đánh giá theo từng phần

### Phần 1 – Model Showtime và quan hệ với Movie

- **1.1 Model:** Class **`Showtime`** với các cột `id`, `movie_id` (FK `list_movies.id`), `start_time` (DateTime), `room`; bảng `show_time_movies` qua `__tablename__`; có `relationship` với `Movies`. `db.create_all()` được gọi trong `if __name__ == "__main__"` (main.py). → **Đạt.**

- **1.2 GET /api/movies/\<movie_id\>/showtimes:** Route thực tế là **GET /api/movies/\<id\>/showtime** (số ít). Kiểm tra phim tồn tại → 404 "Movie not found". Trả về list JSON gồm `id`, `movie_id`, `start_time` (isoformat), `room`; sắp xếp theo `Showtime.start_time`. Evidence: list rỗng, có suất chiếu, phim không tồn tại. → **Đạt.**

- **1.3 GET /api/showtimes/\<id\>:** Route thực tế là **GET /api/movies/api/showtime/\<id\>** (do blueprint `api_movie` prefix `/api/movies` và route `/api/showtime/<int:id>`). Có suất chiếu thì trả JSON đủ 4 field; không có thì `{"error": "Showtime not found"}` và 404. → **Đạt.**

### Phần 2 – API tạo và cập nhật (POST, PUT)

- **2.1 POST tạo suất chiếu:** Route **POST /api/movies/\<id\>/showtime** (nested). Body dùng key **`input_start_time`** (đề gợi ý `start_time` — khác tên nhưng rõ ràng). Validation: JSON bắt buộc; `input_start_time` bắt buộc; parse bằng `datetime.fromisoformat`, sai format → 400; phim không tồn tại → 404. Tạo Showtime, commit, trả 201. **Gợi ý:** Response khi tạo hiện chỉ trả `start_time` và `room`, thiếu `id` và `movie_id`; đề yêu cầu "trả về thông tin suất chiếu vừa tạo" — nên thêm `id`, `movie_id` vào response. Token bắt buộc (401 nếu thiếu). Evidence: tạo thành công, thiếu start_time, format sai. → **Đạt.**

- **2.2 PUT /api/showtimes/\<id\>:** Route thực tế **PUT /api/movies/api/showtime/\<id\>**. Kiểm tra token; lấy showtime theo id. **Lỗi nhỏ:** Khi showtime **không tồn tại**, code trả `{"error": "Movie not found"}` thay vì `{"error": "Showtime not found"}` (dòng 232 trong api_movie.py). Nên sửa thành "Showtime not found". Phần còn lại: đọc body, partial update (`input_start_time`, `room`, `movie_id`); validate format datetime và movie_id tồn tại; trả 200 với thông tin sau cập nhật. → **Đạt** (trừ lỗi message 404 nêu trên).

### Phần 3 – Xóa (DELETE)

- **3.1 DELETE /api/showtimes/\<id\>:** Route thực tế **DELETE /api/movies/api/showtime/\<id\>**. Có showtime thì xóa, commit, trả `{"message": "Showtime deleted"}` 200; không có thì 404 `{"error": "Showtime not found"}`. Token bắt buộc. Evidence: xóa thành công và id không tồn tại. → **Đạt.**

### Bảo vệ bằng token

- Toàn bộ route showtime (GET nested, POST, GET by id, PUT, DELETE) đều yêu cầu token; không token trả 401. Đề nêu token là tùy chọn; việc bảo vệ cả GET là mở rộng chấp nhận được. → **Đạt.**

---

## 3. Điểm mạnh

- Đủ evidence cho nhiều tình huống: list rỗng/có dữ liệu, phim không tồn tại, tạo thành công và lỗi (thiếu start_time, format sai), GET by id (có/không), PUT thành công và movie_id không tồn tại, DELETE thành công/404.
- Model Showtime đúng cấu trúc, có foreign key và relationship với Movies.
- Validation rõ: start_time bắt buộc, format ISO (fromisoformat), kiểm tra phim tồn tại; PUT kiểm tra movie_id tồn tại.
- Tên class, key JSON dùng tiếng Anh (`movie_id`, `start_time`, `room`, `error`, `message`). Trả `start_time` dạng ISO qua `.isoformat()`.
- Cập nhật PUT đúng kiểu partial update (chỉ đổi field client gửi).

---

## 4. Gợi ý cải thiện (không trừ điểm)

- **URL route:** Đề gợi ý `/api/showtimes/<id>` cho GET/PUT/DELETE một suất chiếu; hiện dùng `/api/movies/api/showtime/<id>` (do gắn chung blueprint movies). Nếu muốn đúng đề có thể tách blueprint `api_showtime` với prefix `/api/showtimes`, hoặc giữ nguyên vì vẫn đủ chức năng.
- **Tên path:** Đề dùng "showtimes" (số nhiều); code dùng "showtime" (số ít). Có thể thống nhất "showtimes" cho resource collection.
- **Body key:** Đề gợi ý `start_time`; code dùng `input_start_time`. Có thể đổi sang `start_time` để đồng nhất với response và tài liệu API.
- **Response POST:** Khi tạo suất chiếu thành công nên trả đủ `id`, `movie_id`, `start_time`, `room` (hiện thiếu `id`, `movie_id`).
- **PUT khi không tìm thấy showtime:** Sửa message 404 từ "Movie not found" thành "Showtime not found".

---

## 5. Kết luận

- **Hoàn thành:** Đủ Phần 1 (model Showtime, GET nested, GET by id), Phần 2 (POST nested, PUT), Phần 3 (DELETE); có bảo vệ bằng token cho toàn bộ API showtime.
- **Evidence:** Đủ và phù hợp với từng nhóm endpoint (thành công và lỗi).
- **Đánh giá:** **Đạt** — bài tập số 4 (API cho Suất chiếu) hoàn thành tốt. Chỉ cần lưu ý sửa message 404 khi showtime không tồn tại (PUT) và bổ sung id, movie_id vào response POST nếu muốn đúng chuẩn "trả về thông tin suất chiếu vừa tạo".

Chúc em tiếp tục làm tốt các bài tiếp theo.
