# PHẦN MỀM QUẢN LÝ BÃI ĐỖ XE THÔNG MINH

## 1. Giới thiệu đề tài

Đề tài xây dựng phần mềm quản lý bãi đỗ xe thông minh bằng ngôn ngữ Python.  
Phần mềm hỗ trợ quản lý vị trí trống trong bãi xe, ghi nhận thời gian gửi xe thực tế, tính toán chi phí gửi xe và lưu dữ liệu vào cơ sở dữ liệu SQLite.

## 2. Chức năng chính

- Quản lý danh sách vị trí đỗ xe.
- Kiểm tra vị trí còn trống hoặc đã có xe.
- Gửi xe vào bãi và lưu thời gian bắt đầu.
- Lấy xe ra khỏi bãi.
- Tính tiền gửi xe dựa trên thời gian gửi thực tế.
- Lưu lịch sử gửi xe trong database.
- Hiển thị thông tin xe, vị trí, thời gian và chi phí.

## 3. Công nghệ sử dụng

- Python
- Tkinter
- SQLite
- Lập trình hướng đối tượng OOP

## 4. Cấu trúc chương trình

- `main.py`: Chạy giao diện chính của phần mềm.
- `models.py`: Định nghĩa các lớp đối tượng như Vehicle, ParkingSlot, ParkingLot.
- `database.py`: Xử lý lưu trữ dữ liệu với SQLite.
- `requirements.txt`: Danh sách thư viện cần cài đặt.
- `smart_parking.db`: File cơ sở dữ liệu của chương trình.

## 5. Hướng dẫn chạy chương trình

Bước 1: Cài đặt Python.

Bước 2: Mở thư mục project bằng PyCharm hoặc VS Code.

Bước 3: Cài thư viện cần thiết:

pip install -r requirements.txt

Bước 4: Chạy chương trình:
python main.py

## 6. Hình ảnh minh họa
Giao diện chính

Chức năng gửi xe

Chức năng lấy xe và tính tiền

## 7. Sinh viên thực hiện
Họ và tên: Nguyễn Văn Tuyến

Lớp: K59.KMT.K01

Mã sinh viên: K235480106077

Giáo viên hướng dẫn: Nguyễn Tuấn Linh
