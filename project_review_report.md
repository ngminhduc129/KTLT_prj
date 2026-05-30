# KTLT_prj - Project Review Report

> Banking Account Management System (Python)
> Generated: 30/05/2026
> Total files: 27 (~2,500 LOC)
> Structure: Models → Structures → Services → Persistence

---

## Table of Contents

1. [Runtime Crash (7 lỗi)](#1-runtime-crash)
2. [Logic Bugs (4 lỗi)](#2-logic-bugs)
3. [Dead Code & Unused Code (7 mục)](#3-dead-code)
4. [PEP 8 - Class Naming Violations (6 class)](#4-pep-8-naming-violations)
5. [Minor / Cosmetic Issues (8 mục)](#5-minor-issues)
6. [File Inventory](#6-file-inventory)
7. [Test Status](#7-test-status)
8. [Architecture - Persistence Disconnected](#8-architecture-persistence-disconnected)

---

## 1. Runtime Crash

> Các lỗi gây `TypeError` ngay khi chạy đến code đó.

### 🔴 #1 — `SavingDeposit(...)` thiếu `close_date`

| File | Dòng |
|------|------|
| `Services/saving_service.py` | 36-46 |

```python
# Tạo SavingDeposit thiếu tham số close_date
new_saving = SavingDeposit(
    saving_id, owner_account_id, full_name, user_id, amount, term, start_date,
    maturity_date=None,        # param thứ 8
    status="ACTIVE"            # param thứ 10 — bỏ qua param thứ 9 (close_date)
)
# => TypeError: __init__() missing 1 required positional argument: 'close_date'
```

**Fix:** Thêm `close_date=None` vào constructor call.

---

### 🔴 #2 — `Hash_table.insert()` thiếu key

| File | Dòng |
|------|------|
| `Services/saving_service.py` | 49 |

```python
self.saving_storage.insert(new_saving)
# Hash_table.insert(self, key, value) cần 2 args, chỉ có 1
# => TypeError: insert() missing 1 required positional argument: 'value'
```

**Fix:** `self.saving_storage.insert(saving_id, new_saving)`

---

### 🔴 #3 — `LinkedList.append()` thiếu value

| File | Dòng |
|------|------|
| `Services/account_service.py` | 194 |

```python
accounts_of_user_id.append(account)
# LinkedList.append(self, key, value) cần 2 args, chỉ có 1
# => TypeError: append() missing 1 required positional argument: 'value'
```

**Fix:** `accounts_of_user_id.append(account.account_id, account)`

---

### 🔴 #4 — `Hash_table.values()` gọi `append()` thiếu value

| File | Dòng |
|------|------|
| `Structures/Hash_table.py` | 105-106 |

```python
def values(self):
    result = LinkedList()
    for bucket in self.table:
        current = bucket
        while current is not None:
            result.append(current.value)   # thiếu key
    return result
```

Gây crash khi gọi `get_all_users()`, `get_all_accounts()`, `get_all_savings()`.

**Fix:** `result.append(current.key, current.value)`

---

### 🔴 #5 — Gọi `deposit()` sai số lượng tham số

| File | Dòng |
|------|------|
| `Services/bank_service.py` | 385, 427 |

```python
# bank_service.py gọi với 4 tham số:
self.account_service.deposit(account_id, pin, interest, password)
self.account_service.deposit(account_id, pin, final_received_money, password)

# Nhưng AccountService.deposit() chỉ nhận 3:
def deposit(self, account_id, pin, amount):
# => TypeError
```

**Fix:** Cập nhật signature của `deposit()` thêm `password`, hoặc sửa cách gọi.

---

### 🔴 #6 — `show_statement()` thiếu `self`

| File | Dòng |
|------|------|
| `Services/bank_service.py` | 454 |

```python
def show_statement():   # thiếu self
    pass
# => TypeError: show_statement() takes 0 positional arguments but 1 was given
```

**Fix:** `def show_statement(self):`

---

### 🔴 #7 — Test gọi `deposit()`/`withdraw()` sai signature

| File | Dòng |
|------|------|
| `Services/Tests/test_account_service.py` | 90, 100, 113, 124 |

Các test call:
```python
self.service.deposit("ACC01", "1234", 200.0, "pass123")    # 4 args
self.service.withdraw("ACC01", "1234", 300.0, "pass123")    # 4 args
```

Nhưng `deposit`/`withdraw` hiện tại chỉ nhận 3 args → **4 tests sẽ FAIL**.

---

## 2. Logic Bugs

### 🟠 #8 — Status mismatch: `"ACTIVE"` vs `"Active"`

| File | Dòng |
|------|------|
| `Services/saving_service.py` | 46, 111 |

```python
# Tạo: status = "ACTIVE"      (ALL CAPS)
# Check: if status == "Active"  (Capitalized)
# => Không bao giờ match — get_active_savings() luôn rỗng
```

**Fix:** `if active.status == "ACTIVE":`

---

### 🟠 #9 — Công thức tính lãi sai

| File | Dòng |
|------|------|
| `Services/saving_service.py` | 59 |

```python
months = (maturity.year - start.year) * 12 + (maturity.month - start.month)
if months < start.day:     # so sánh tháng với ngày???
    months -= 1
```

`months` là số tháng (0, 1, 12,...), `start.day` là ngày trong tháng (1-31). So sánh này vô nghĩa.

**Fix:** `if maturity.day < start.day: months -= 1`

---

### 🟠 #10 — Trạng thái không nhất quán

| File | Dòng |
|------|------|
| `Services/account_service.py` | 40, 240, 265 |

```python
# 2 giá trị cho cùng 1 trạng thái "đang mở":
status = "Active"   # khi tạo
status = "Unlock"   # khi mở khoá

# unlock_account() kiểm tra:
if account.status == "Unlock": raise...  # bỏ sót account "Active"
```

**Fix:** Dùng 1 giá trị chuẩn: `"Active"` = mở, `"Lock"` = khoá.

---

### 🟠 #11 — Không check trạng thái Lock trước giao dịch

| File | Dòng |
|------|------|
| `Services/account_service.py` | 67, 89 |

```python
def deposit(self, account_id, pin, amount):
    # ... không kiểm tra account có bị Lock không
    account.balance += amount   # tài khoản khoá vẫn giao dịch được
```

**Fix:** Thêm `if account.status == "Lock": raise ValueError("Account is locked")`

---

## 3. Dead Code

| # | File | Dòng | Mô tả |
|---|------|------|-------|
| 🟡12 | `Persistence/` | all | **Toàn bộ 4 repository không được Service nào gọi** — dữ liệu không bao giờ lưu file |
| 🟡13 | `Structures/Linked_list.py` | 38-46 | `find()` không được dùng ở đâu |
| 🟡14 | `Services/transaction_service.py` | 83-93 | Code test lẫn trong file production (`if __name__` block) |
| ⚪15 | `Services/bank_service.py` | 5-13 | Import `User`, `SavingDeposit`, `Transaction`, 4 repository — không dùng |
| ⚪16 | `Models/account.py` | 1 | `from datetime import date` — không dùng |
| ⚪17 | `Models/transaction.py` | 1 | `from datetime import date` — không dùng |
| ⚪18 | `Models/saving_deposit.py` | 1 | `from datetime import date` — không dùng |

---

## 4. PEP 8 - Class Naming Violations

| File | Tên hiện tại | Phải là |
|------|-------------|---------|
| `Structures/Hash_table.py` | `Hash_table` | `HashTable` |
| `Persistence/Base_repository.py` | `Base_repository` | `BaseRepository` |
| `Persistence/User_repository.py` | `User_repository` | `UserRepository` |
| `Persistence/Account_repository.py` | `Account_repository` | `AccountRepository` |
| `Persistence/Transaction_repository.py` | `Transaction_repository` | `TransactionRepository` |
| `Persistence/Saving_repository.py` | `Saving_repository` | `SavingRepository` |

---

## 5. Minor Issues

- `Models/transaction.py:20-26` — `self.timestamp` gán 2 lần (dòng 20 vô ích)
- `Services/account_service.py:185` — `"No users found"` phải là `"No accounts found"`
- `Services/account_service.py:187` — Còn comment chat: `"DNB design not sure correct so NMD dung le nha le nhe"`
- `Services/account_service.py:240,265` — `"already unlock"`/`"already Lock"` → `"already unlocked"`/`"already locked"`
- `readme.md:144` — Nhầm `saving_account.py` → `saving_deposit.py`
- `readme.md:470-491` — Nhắc `menu.py`, `main.py` — không tồn tại
- `.gitignore:22` — ignore `**/Tests/` nhưng đã commit file test
- `Services/bank_service.py` — Nhiều lỗi chính tả: `import agian`, `neccessary infromation`, `targer`, ...

---

## 6. File Inventory

```
KTLT_prj/
├── .gitignore
├── readme.md
├── .vscode/
│   └── settings.json
├── Models/
│   ├── __init__.py
│   ├── user.py
│   ├── account.py
│   ├── transaction.py
│   └── saving_deposit.py
├── Structures/
│   ├── __init__.py
│   ├── Node.py
│   ├── Linked_list.py
│   └── Hash_table.py
├── Persistence/
│   ├── Base_repository.py
│   ├── File_handler.py
│   ├── User_repository.py
│   ├── Account_repository.py
│   ├── Transaction_repository.py
│   └── Saving_repository.py
├── Services/
│   ├── __init__.py
│   ├── user_service.py
│   ├── account_service.py
│   ├── transaction_service.py
│   ├── saving_service.py
│   ├── bank_service.py
│   └── Tests/
│       ├── test_user_service.py
│       ├── test_account_service.py
│       └── test_transaction_service.py
└── data/                 (empty)
```

**Total: 27 files (~2,500 LOC)**

---

## 7. Test Status

| Test file | Cases | Trạng thái |
|-----------|-------|------------|
| `test_user_service.py` | 8 | ✅ OK |
| `test_account_service.py` | 12 | ❌ 4 tests fail (sai số lượng tham số) |
| `test_transaction_service.py` | 4 | ✅ OK |
| **Total** | **25** | **21 pass, 4 fail** |

**Missing test coverage:**
- `UserService`: `display_all_users()`, `get_all_users()`
- `AccountService`: `find_account()`, `generate_account_id()`, `get_all_accounts()`
- `TransactionService`: `get_transactions_by_account()`, `get_transactions_by_date()`, `get_all_transactions()`
- `SavingService`: toàn bộ methods

---

## 8. Architecture — Persistence Disconnected

### Hiện tại

```
UserService (Hash_table in RAM)    ╳    User_repository -> data/users.txt
AccountService (Hash_table in RAM) ╳    Account_repository -> data/accounts.txt
SavingService (Hash_table in RAM)  ╳    Saving_repository -> data/savings.txt
TrxService (LinkedList in RAM)     ╳    Trx_repository -> data/transactions.txt
```

`╳` = **không kết nối**. Persistence layer tồn tại nhưng không ai gọi.

### Hậu quả

- Toàn bộ dữ liệu chỉ trong RAM — **mất hết khi tắt chương trình**
- Thư mục `data/` rỗng

### Đề xuất

Tích hợp repository vào mỗi Service:
1. Trong `__init__`: gọi `load_data()` để nạp dữ liệu từ file
2. Trong `create_*`: gọi `append_data(obj)`
3. Trong `update_*` / `delete_*`: gọi `save_data()` (ghi đè toàn bộ)
4. Thêm `save_hash_table()` vào `Base_repository` để ghi Hash_table xuống file

---

> **End of Report**
