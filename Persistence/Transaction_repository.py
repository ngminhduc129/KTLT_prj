from Persistence.Base_repository import Base_repository
# Import lớp Model Transaction đại diện cho cấu trúc dữ liệu của một Giao dịch
from Models.transaction import Transaction  

class Transaction_repository(Base_repository):
    """
    Lớp quản lý lưu trữ dành riêng cho thực thể Transaction (Nhật ký/Lịch sử giao dịch).
    Kế thừa toàn bộ cơ chế I/O từ Base_repository để tái sử dụng mã nguồn (DRY).
    """
    def __init__(self):
        # Sử dụng super() để gọi hàm __init__ của lớp cha (Base_repository).
        # Cung cấp 2 tham số cụ thể để "cá nhân hóa" thao tác cho Giao dịch:
        # 1. 'data/transactions.txt': Tên file text dùng để lưu trữ toàn bộ lịch sử giao dịch.
        # 2. Transaction: Truyền trực tiếp Class Transaction lên cho Base_repository,
        #    đóng vai trò như một Factory để lớp cha tự động biến các chuỗi text 
        #    thành các đối tượng Transaction khi thực thi hàm load_data().
        super().__init__('data/transactions.txt', Transaction)
        