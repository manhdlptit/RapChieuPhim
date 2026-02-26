# Báo cáo kiểm tra chất lượng code – RapChieuPhim

Kiểm tra file **`main.py`** (Flask app, API User, API Movies).

---

## 1. Bảo mật (Security)

### 1.1 Nghiêm trọng

| Vấn đề | Vị trí | Mô tả |
|--------|--------|--------|
| **Mật khẩu lưu dạng plaintext** | `User` model, `login`, `create_user` | Mật khẩu đang lưu và so sánh trực tiếp trong DB. Nên dùng **hash** (ví dụ `werkzeug.security.generate_password_hash` và `check_password_hash`) để lưu và kiểm tra. |
| **SECRET_KEY hardcode** | Dòng 7 | `app.config["SECRET_KEY"] = 'manhdl'` dễ lộ khi đẩy code. Nên đọc từ biến môi trường: `os.environ.get("SECRET_KEY", "default-for-dev")`. |

### 1.2 Nên cải thiện

- **Login API:** Trả "Invalid email" vs "Invalid password" giúp kẻ tấn công đoán được email có tồn tại. Nên dùng chung một message: `"Invalid email or password"`.

---

## 2. Lỗi tiềm ẩn (Bugs)

### 2.1 Có thể gây crash / 500

| Vấn đề | Vị trí | Cách sửa |
|--------|--------|----------|
| **`request.form["email"]`** | Dòng 59 | Thiếu key sẽ gây **KeyError**. Nên dùng `request.form.get("email")` rồi kiểm tra `if not email`. |
| **`request.form["password"]`** | Dòng 62 | Tương tự, nên dùng `.get("password")` và kiểm tra. |
| **`header.split(" ")[1]`** | Dòng 170 | Nếu client gửi `Authorization: Bearer` (không có token), `split(" ")[1]` gây **IndexError**. Nên kiểm tra `len(parts) >= 2` sau khi `split(" ")`. |
| **`data = request.get_json()`** | create_user, create_token, create_movies, update_user, update_movie | Nếu client không gửi JSON (hoặc Content-Type sai), `get_json()` có thể trả **None**. Gọi `data.get(...)` khi `data is None` sẽ **AttributeError**. Nên: `data = request.get_json()` rồi `if data is None: return jsonify({"error": "Invalid JSON"}), 400`. |
| **`create_movies`: `title.strip()`** | Dòng 337 | Khi `title` là số (ví dụ client gửi `"title": 123`), `title.strip()` gây **AttributeError**. Nên ép string: `str(title).strip()` hoặc kiểm tra `isinstance(title, str)`. |

### 2.2 Lỗi logic

| Vấn đề | Vị trí | Mô tả |
|--------|--------|--------|
| **Session set trước khi validate** | `sign_up` dòng 36 | `session["email"] = email` được gán ngay khi POST, trước khi kiểm tra email/name trùng. Nếu sau đó flash lỗi và render lại form, session vẫn có email — dễ gây nhầm lẫn. Nên chỉ set session sau khi tạo user thành công (hoặc không set ở đây vì đang redirect sang login). |
| **PUT user – trùng name** | `update_user` dòng 224 | `User.query.filter((User.name==name)).first()` không loại trừ user hiện tại. Nếu user **giữ nguyên tên** (gửi đúng name cũ), `found_name_same` là chính họ → trả 400 "name existed" sai. Nên thêm điều kiện: `User.id != found_id.id`. |
| **create_user khi exception** | Dòng 161 | `return {"error": str(a)}` trả **dict**, không phải Response, và **không có status code**. Nên: `return jsonify({"error": str(a)}), 500`. |

### 2.3 Thiếu nhất quán API

- **POST /api/movies** khi tạo thành công nên trả **201 Created**; hiện không truyền status nên mặc định 200.

---

## 3. Cấu trúc và tổ chức code

| Vấn đề | Gợi ý |
|--------|--------|
| **Một file quá dài** | `main.py` ~420 dòng, gồm model, route web, route API User, API Movies. Nên tách: `models.py` (User, Movies), `routes/web.py`, `routes/api_users.py`, `routes/api_movies.py`, hoặc dùng Flask Blueprint. |
| **Tên biến dễ nhầm** | `sign_up`: `found_email = User.query.filter_by(name=name).first()` — biến là user tìm theo **name** nhưng tên biến là "email". Nên đặt `found_user_by_name` hoặc tương tự. |
| **Điều kiện thừa** | `call_api_users_with_id`: đã `if user is None: return 401`; phía dưới `if user is not None:` luôn đúng, có thể bỏ bớt để code gọn. |

---

## 4. Xử lý lỗi và validation

| Vấn đề | Vị trí | Gợi ý |
|--------|--------|--------|
| **except Exception quá rộng** | print_user, print_id_user, update_user, delete_user, found_user | Bắt `Exception` dễ che lỗi lập trình. Nên bắt cụ thể (ví dụ `SQLAlchemyError`) hoặc chỉ dùng ở tầng ngoài, còn bên trong để lỗi nổi lên trong môi trường dev. |
| **Thiếu kiểm tra body JSON** | create_user, create_token, create_movies, update_user, update_movie | Luôn kiểm tra `data = request.get_json(); if data is None: return 400`. |
| **API search user** | found_user | Khi không truyền `email` trả 404; khi có email nhưng không tìm thấy trả 400. Nên thống nhất (ví dụ 400 cho thiếu param, 404 cho "user not found") và ghi rõ trong tài liệu API. |

---

## 5. Chuẩn code (PEP 8 / style)

| Vấn đề | Ví dụ | Gợi ý |
|--------|--------|--------|
| **So sánh với None** | `Movies.duration_minutes != None` | PEP 8 khuyến nghị dùng `is not None`. |
| **Tên biến exception** | `except Exception as a:` | Nên dùng tên rõ hơn: `ex` hoặc `err`. |
| **Khoảng trắng** | `jsonify ({"error":` | Thiếu nhất quán (có chỗ có space sau `jsonify`). Nên thống nhất `jsonify({...})`. |
| **Indentation** | update_user dòng 227–234 | Dùng nhiều level else/indent; có thể rút gọn bằng early return. |

---

## 6. Logic nghiệp vụ (Movies)

| Vấn đề | Vị trí | Mô tả |
|--------|--------|--------|
| **Điều kiện trùng phim** | create_movies dòng 334 | Filter trùng gồm `(Movies.duration_minutes != None) & (Movies.description != None)` — chỉ coi trùng khi cả duration và description đều không NULL. Hai phim cùng title nhưng duration/description NULL sẽ không bị coi là trùng. Nên quyết định rõ: trùng theo **title** hay theo bộ (title, duration, description); nếu chỉ cần title thì chỉ filter theo title. |
| **Kiểu dữ liệu title** | create_movies, update_movie | Nếu client gửi `"title": 123` (số), `len(title.strip())` lỗi. Nên ép `title = data.get("title"); title = str(title).strip() if title is not None else ""` rồi mới kiểm tra rỗng. |

---

## 7. Tóm tắt ưu tiên xử lý

| Mức | Hạng mục |
|-----|-----------|
| **Cao** | Hash mật khẩu; không hardcode SECRET_KEY; xử lý `data = request.get_json()` khi None; sửa PUT user khi giữ nguyên name (filter loại trừ user hiện tại); sửa `create_user` exception trả jsonify + status. |
| **Trung bình** | Tránh KeyError với `request.form.get("email")`, `request.form.get("password")`; bảo vệ `Authorization` split (kiểm tra len); kiểm tra kiểu/None cho title trước khi .strip(); POST /api/movies trả 201. |
| **Thấp** | Tách file / Blueprint; đổi tên biến exception; dùng `is not None`; thống nhất message login; rút gọn điều kiện thừa. |

---

## 8. Kết luận

- **Điểm mạnh:** Đủ tính năng API User và Movies, có validation cơ bản, phân tách helper function, dùng đúng status code ở nhiều chỗ.
- **Cần cải thiện:** Bảo mật (password, SECRET_KEY), xử lý body/header thiếu hoặc sai kiểu, vài lỗi logic (PUT user trùng name, exception create_user), thống nhất style và cấu trúc file.

Ưu tiên xử lý nhóm **bảo mật** và **lỗi có thể gây 500** trước, sau đó đến logic và cấu trúc code.
