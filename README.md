# Đối chiếu File Excel Giao Dịch Viên

**Tác giả:** Bùi Thế Phong  
**Liên hệ:** phong@poc.asia

---

## Giới thiệu
Ứng dụng giúp đối chiếu số lượng giữa hai file Excel (file KRX và file báo cáo gửi VSD) một cách tự động, nhanh chóng và chính xác. Ứng dụng phù hợp cho các bạn không chuyên IT, chỉ cần click và chạy, không cần cài đặt Python hay thư viện nào khác.

- Giao diện thân thiện, dễ sử dụng.
- Hỗ trợ upload 2 file Excel, nhập thông tin cột, tỷ lệ chuyển đổi.
- Tự động so sánh, phát hiện sai khác, xuất báo cáo chi tiết.
- Có thể chạy như web app hoặc desktop app (file .exe).

---

## Tính năng chính
- Đối chiếu số lượng giữa hai file Excel theo mã khách hàng.
- Tùy chọn cột, bỏ qua dòng đầu, tỷ lệ chuyển đổi.
- Xuất báo cáo các mã bị lệch số lượng, nêu rõ nguyên nhân.
- Giao diện đẹp, dễ thao tác, có hiệu ứng pháo hoa khi hoàn thành.
- Đóng gói thành file .exe, chỉ cần click để chạy.

---

## Hướng dẫn sử dụng
### 1. Dùng dưới dạng web app (yêu cầu Python)
```sh
pip install -r requirements.txt
uvicorn main:app --reload
```
Truy cập: http://localhost:8000

### 2. Dùng dưới dạng desktop app (không cần cài Python)
- Chạy file `DoiChieuExcel.exe` trong thư mục `dist`.
- Đảm bảo có đủ các thư mục: `templates`, `static`, `uploads` cùng cấp với file `.exe`.
- Giao diện sẽ hiện ra, thao tác như web app.

### 3. Hướng dẫn sử dụng chức năng
- Chọn 2 file Excel cần đối chiếu.
- Nhập tên cột hoặc ký tự cột, số dòng bỏ qua, tỷ lệ chuyển đổi.
- Nhấn "So sánh và xuất báo cáo".
- Tải file báo cáo sai khác nếu có.

---

## Hướng dẫn build file .exe (đóng gói desktop app)

1. **Cài đặt các thư viện cần thiết:**
   ```sh
   pip install -r requirements.txt
   pip install pyinstaller pywebview
   ```
2. **Kiểm tra chắc chắn đã có các thư mục:**
   - `templates/` (chứa file HTML)
   - `static/` (có thể trống)
   - `uploads/` (có thể trống)
   - `icon.ico` (nếu muốn có icon cho app)
3. **Tạo file spec (nếu cần tuỳ chỉnh), hoặc build nhanh bằng lệnh:**
   ```sh
   pyinstaller --noconsole --onefile --add-data "templates;templates" --add-data "static;static" --add-data "uploads;uploads" --icon=icon.ico desktop.py
   ```
   - Nếu dùng lệnh trên mà bị lỗi, hãy tạo file `build.spec` để tuỳ chỉnh kỹ hơn.
4. **Sau khi build xong, file `.exe` sẽ nằm trong thư mục `dist/` cùng với các thư mục phụ trợ.**
5. **Copy toàn bộ thư mục `dist` sang máy khác để sử dụng, không cần cài Python.**

---

## Cấu trúc source code
```
CK/
├── main.py           # Code backend FastAPI xử lý logic đối chiếu
├── desktop.py        # Khởi động app desktop (pywebview)
├── requirements.txt  # Danh sách thư viện Python
├── templates/        # Giao diện HTML (index.html, result.html)
├── static/           # Thư mục chứa file tĩnh (nếu có)
├── uploads/          # Thư mục lưu file upload và báo cáo
├── icon.ico          # Icon cho app (nếu có)
└── ...
```

---

## Đóng góp & liên hệ
Mọi ý kiến đóng góp, vui lòng liên hệ:
- **Bùi Thế Phong**  
- Email: phong@poc.asia 