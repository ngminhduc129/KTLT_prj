# KTLT - Banking Account Management System

## Giới thiệu
Đây là đồ án mô phỏng một hệ thống quản lý tài khoản ngân hàng viết bằng **Python** với kiến trúc nhiều tầng.
Dự án **tự cài đặt** các cấu trúc dữ liệu/thuật toán cơ bản (ví dụ: **Linked List**, **Hash Table**) thay vì dùng sẵn các cấu trúc nâng cao như `dict`, `set`, `list`.

## Kiến trúc dự án

- `Models/`: định nghĩa thực thể dữ liệu (User, Account, Transaction, SavingDeposit...)
- `Structures/`: cấu trúc dữ liệu tự cài đặt (Node, Linked_list, Hash_table...)
- `Services/`: xử lý nghiệp vụ (UserService, AccountService, TransactionService, SavingService, BankService...)
- `Persistence/`: cơ chế đọc/ghi file text (repositories, File_handler...)
- `UI/`: giao diện người dùng (PyQt) qua `MainWindow` và các trang trong `UI/pages/`

## Tính năng chính
- Quản lý khách hàng (thêm/xem/cập nhật/tìm kiếm)
- Quản lý tài khoản (tạo tài khoản, đăng nhập, xác thực PIN, khóa/mở khóa, đổi PIN)
- Giao dịch ngân hàng (nạp tiền, rút tiền, chuyển khoản nội bộ)
- Tính lãi suất sổ tiết kiệm
- Xem lịch sử & sao kê theo giao dịch

## Cách chạy
1. Cài dependencies (nếu chưa có):
   - PyQt5
2. Chạy ứng dụng:
   ```bash
   python main.py
   ```

## Cấu trúc file quan trọng
```text
KTLT_prj/
├── main.py
├── readme.md
├── Models/
│   ├── user.py
│   ├── account.py
│   ├── transaction.py
│   └── saving_deposit.py
├── Structures/
│   ├── Node.py
│   ├── Linked_list.py
│   └── Hash_table.py
├── Persistence/
│   ├── File_handler.py
│   ├── Base_repository.py
│   ├── User_repository.py
│   ├── Account_repository.py
│   ├── Transaction_repository.py
│   └── Saving_repository.py
├── Services/
│   ├── user_service.py
│   ├── account_service.py
│   ├── transaction_service.py
│   ├── saving_service.py
│   └── bank_service.py
├── UI/
│   ├── main_window.py
│   └── pages/
│       ├── home_page.py
│       ├── account_page.py
│       └── ...
├── data/   (dữ liệu file, tùy cấu hình dự án)
└── project_review_report.md
```

## Ghi chú
- Dữ liệu có thể được lưu/đọc qua lớp `Persistence/`.
- Giao diện hiện tại dùng PyQt5.

