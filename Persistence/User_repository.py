from Persistence.Base_repository import Base_repository
# Import lớp Model User (chứa logic cấu trúc dữ liệu của khách hàng)
from Models.user import User  

class User_repository(Base_repository):
    """
    Lớp quản lý lưu trữ dành riêng cho thực thể User (Khách hàng).
    Kế thừa  toàn bộ tính năng load_data, save_data, append_data từ Base_repository.
    """
    def __init__(self):
        # Gọi hàm khởi tạo __init__ của lớp cha (Base_repository)
        # Truyền vào 2 tham số đặc thù của User:
        # 1. 'data/users.txt': Đường dẫn tới file text lưu dữ liệu khách hàng.
        # 2. User: Truyền chính Class User (không phải object) lên cho lớp cha,
        #    để lớp cha biết cách khởi tạo đối tượng User khi đọc từng dòng trong file.
        super().__init__('data/users.txt', User)