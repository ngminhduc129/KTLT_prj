# Hệ Thống Quản Lý Tài Khoản Ngân Hàng

## Giới thiệu

Đây là đồ án mô phỏng một hệ thống quản lý tài khoản ngân hàng.  
Điểm đặc biệt của dự án là **không sử dụng các cấu trúc dữ liệu và thư viện quản lý có sẵn** như `dict`, `set`, `list` nâng cao hoặc ORM/database framework.

Toàn bộ hệ thống được xây dựng thủ công từ đầu, bao gồm:

- Linked List
- Hash Table
- Node
- Quản lý lưu trữ file text
- Thuật toán tìm kiếm và xử lý dữ liệu

Hệ thống được thiết kế theo mô hình nhiều tầng:

- **Model Layer**
- **Structure Layer**
- **Service Layer**
- **Persistence Layer**
- **UI Layer**

---

# Tính Năng Chính

## 1. Quản lý khách hàng / chủ thẻ

- Thêm khách hàng mới
- Xem danh sách khách hàng
- Cập nhật thông tin khách hàng
- Tìm kiếm khách hàng theo ID

---

## 2. Quản lý tài khoản

- Tạo tài khoản ngân hàng
- Đăng nhập hệ thống
- Xác thực bằng mã PIN
- Gán tài khoản với khách hàng
- Khóa / mở khóa tài khoản
- Đổi mã PIN

---

## 3. Giao dịch ngân hàng

- Nạp tiền
- Rút tiền
- Chuyển khoản nội bộ
- Kiểm tra số dư

---

## 4. Tính lãi suất

- Tính lãi suất không kỳ hạn theo tháng
- Cập nhật số dư tự động

---

## 5. Báo cáo và sao kê

- Xem lịch sử giao dịch
- Lọc giao dịch theo khoảng thời gian
- In sao kê tài khoản

---

# Phân Tích Thực Thể

---

# 1. Thực Thể User (Khách Hàng)

| Thuộc tính | Kiểu dữ liệu | Mô tả |
|---|---|---|
| user_id | String | Mã khách hàng |
| full_name | String | Họ tên |
| phone | String | Số điện thoại |
| email | String | Email |
| sex | String | Giới tính |
| address | String | Địa chỉ |
| job | String | Nghề nghiệp |
| dob | String | Ngày sinh |
| rank | String | Hạng khách hàng |

---

# 2. Thực Thể Account (Tài Khoản)

| Thuộc tính | Kiểu dữ liệu | Mô tả |
|---|---|---|
| account_id | String | Mã tài khoản |
| balance | Float | Số dư |
| pin | String | Mã PIN |
| user_id | String | Mã khách hàng |
| password | String | Mật khẩu |
| status | String | Trạng thái |
| created_at | String | Ngày tạo |

---

# 3. Thực Thể Transaction (Giao Dịch)

| Thuộc tính | Kiểu dữ liệu | Mô tả |
|---|---|---|
| trans_id | String | Mã giao dịch |
| from_account | String | TK gửi |
| to_account | String | TK nhận |
| type_trans | String | Loại giao dịch |
| amount | Float | Số tiền |
| timestamp | String | Thời gian |
| description | String | Nội dung |

---

# 4. Thực Thể SavingDeposit (Sổ Tiết Kiệm)

| Thuộc tính | Kiểu dữ liệu | Mô tả |
|---|---|---|
| deposit_id | String | Mã sổ |
| owner_account_id | String | Tài khoản sở hữu |
| amount | Float | Số tiền gửi |
| interest_rate | Float | Lãi suất |
| term_months | Integer | Kỳ hạn |
| start_date | String | Ngày gửi |
| maturity_date | String | Ngày đáo hạn |
| status | String | Trạng thái |

---

# Kiến Trúc Hệ Thống

```text
project/
│
├── models/
│   ├── user.py
│   ├── account.py
│   ├── transaction.py
│   └── saving_account.py
│
├── structures/
│   ├── linked_list.py
│   ├── hash_table.py
│   └── node.py
│
├── services/
│   ├── user_service.py
│   ├── account_service.py
│   ├── transaction_service.py
│   ├── saving_service.py
│   └── bank_service.py
│
├── persistence/
│   ├── user_repository.py
│   ├── account_repository.py
│   ├── transaction_repository.py
│   └── saving_repository.py
│
├── ui/
│   └── menu.py
│
└── main.py
```

---

# Thiết Kế Models

## Class User

### Chức năng

- Quản lý thông tin khách hàng
- Chuyển object sang chuỗi để lưu file
- Parse dữ liệu từ file

### Các phương thức

```python
__init__()
display_info()
to_file_string()
from_file_string()
```

---

## Class Account

### Chức năng

- Quản lý tài khoản ngân hàng
- Kiểm tra mã PIN
- Quản lý số dư

### Các phương thức

```python
__init__()
check_pin()
display_info()
to_file_string()
from_file_string()
```

---

## Class Transaction

### Chức năng

- Quản lý thông tin giao dịch
- Lưu lịch sử giao dịch

### Các phương thức

```python
__init__()
display_info()
to_file_string()
from_file_string()
```

---

## Class SavingDeposit

### Chức năng

- Quản lý sổ tiết kiệm
- Tính lãi suất
- Theo dõi trạng thái sổ

### Các phương thức

```python
__init__()
display()
to_file_string()
from_file_string()
```

---

# Structures

## Class Node

### Vai trò

Node được sử dụng cho:

- Linked List
- Hash Bucket

### Thuộc tính

```python
data
next
```

---

## Class LinkedList

### Chức năng

- Lưu danh sách động
- Quản lý giao dịch
- Hỗ trợ Hash Table bucket

### Các phương thức

```python
append()
prepend()
remove()
find()
display()
is_empty()
length()
```

---

## Class HashTable

### Chức năng

- Lưu dữ liệu theo key-value
- Tăng tốc tìm kiếm tài khoản và khách hàng

### Các phương thức chính

```python
hash_function()
insert()
remove()
search()
display()
```

---

# Service Layer

## UserService

### Vai trò

Quản lý thông tin khách hàng.

### Cấu trúc sử dụng

```python
HashTable
```

### Chức năng

```python
create_user()
find_user_by_id()
update_user()
delete_user()
display_all_users()
```

---

## AccountService

### Vai trò

Xử lý các nghiệp vụ tài khoản ngân hàng.

### Cấu trúc sử dụng

```python
HashTable
```

### Chức năng

```python
create_account()
authenticate()
deposit()
withdraw()
transfer()
find_account()
display_all_accounts()
change_pin()
unlock_account()
lock_account()
```

---

## TransactionService

### Vai trò

Quản lý lịch sử giao dịch.

### Cấu trúc sử dụng

```python
LinkedList
```

### Chức năng

```python
add_transaction()
get_transactions_by_account()
get_transactions_by_date()
generate_transaction_id()
```

---

## SavingService

### Cấu trúc sử dụng

```python
LinkedList
```

### Vai trò

Quản lý sổ tiết kiệm.

### Chức năng

```python
create_saving()
calculate_interest()
close_saving()
get_user_savings()
get_active_savings()
generate_saving_id()
```

---

## BankService

### Vai trò

Lớp trung tâm điều phối toàn hệ thống.

### Nhiệm vụ

- Tiếp nhận dữ liệu từ UI Layer
- Điều phối các service khác
- Tổng hợp kết quả xử lý
- Trả dữ liệu về giao diện

### Chức năng

```python
create_customer_and_account()
deposit_money()
withdraw_money()
transfer_money()
show_statement()
```

---

# Persistence Layer

## Vai trò

- Đọc dữ liệu từ file
- Ghi dữ liệu xuống file
- Lưu log hệ thống

---

## Repository

```text
user_repository.py
account_repository.py
transaction_repository.py
saving_repository.py
```

### Các chức năng chính

```python
load_data()
save_data()
append_data()
```

---

# UI Layer

## menu.py

### Vai trò

- Hiển thị menu hệ thống
- Nhận dữ liệu từ người dùng
- Gọi BankService để xử lý

### Ví dụ Menu

```text
1. Tạo khách hàng
2. Tạo tài khoản
3. Đăng nhập
4. Nạp tiền
5. Rút tiền
6. Chuyển khoản
7. Xem sao kê
8. Tạo sổ tiết kiệm
9. Thoát
```

---

# Main Program

## main.py

### Vai trò

- Điểm khởi chạy hệ thống
- Khởi tạo service
- Load dữ liệu
- Chạy menu chính

### Ví dụ

```python
if __name__ == "__main__":
    app = BankService()
    app.run()
```

---

# Kỹ Thuật Được Áp Dụng

## Cấu trúc dữ liệu tự cài đặt

- Linked List
- Hash Table
- Node

---

## Lập trình hướng đối tượng (OOP)

- Encapsulation
- Abstraction
- Composition

---

## Quản lý dữ liệu file text

- Serialize object
- Parse dữ liệu
- Logging transaction

---

# Hướng Phát Triển

- Thêm Database SQL
- Mã hóa PIN bằng SHA256
- Giao diện GUI bằng Tkinter/PyQt
- REST API bằng Flask/FastAPI
- Đăng nhập OTP
- Internet Banking
- Mobile Banking

---

# Kết Luận

Dự án mô phỏng hệ thống ngân hàng giúp:

- Hiểu sâu cấu trúc dữ liệu
- Rèn luyện tư duy thiết kế hệ thống
- Thực hành OOP
- Xây dựng kiến trúc nhiều tầng
- Quản lý dữ liệu thực tế

Đây là một dự án phù hợp để:

- Học Data Structure & Algorithm
- Học Software Design
- Làm đồ án OOP
- Thực hành Python Backend cơ bản