from Persistence.Base_repository import Base_repository
# Import lớp Model Account chứa cấu trúc dữ liệu của Tài khoản ngân hàng
from Models.account import Account  

class Account_repository(Base_repository):
    """
    Lớp quản lý dữ liệu lưu trữ dành riêng cho thực thể Account (Tài khoản).
    Kế thừa toàn bộ tính năng load_data, save_data, append_data từ Base_repository.
    """
    def __init__(self):
        # Hàm super() gọi lên hàm __init__ của lớp cha (Base_repository).
        # Cung cấp 2 tham số cụ thể để "cá nhân hóa" lớp cha cho nghiệp vụ Tài khoản:
        # 1. 'data/accounts.txt': Chỉ định đích danh file lưu trữ thông tin tài khoản.
        # 2. Account: Truyền Lớp (Class) Account để lớp cha sử dụng làm Factory, 
        #    giúp tự động giải mã (deserialize) chuỗi văn bản thành đối tượng Account.
        super().__init__('data/accounts.txt', Account)