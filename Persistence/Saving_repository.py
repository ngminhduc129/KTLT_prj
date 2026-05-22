from Persistence.Base_repository import Base_repository
# Import lớp Model SavingDeposit đại diện cho cấu trúc Sổ tiết kiệm
from Models.saving_deposit import SavingDeposit  

class Saving_repository(Base_repository):
    """
    Lớp quản lý lưu trữ dành riêng cho thực thể SavingDeposit (Sổ tiết kiệm).
    Kế thừa toàn bộ cơ chế đọc/ghi/nối file từ Base_repository.
    """
    def __init__(self):
        # Gọi hàm __init__ của lớp cha (Base_repository).
        # Cung cấp 2 tham số đặc thù cho nghiệp vụ Sổ tiết kiệm:
        # 1. 'data/savings.txt': Đường dẫn file lưu trữ danh sách các sổ tiết kiệm.
        # 2. SavingDeposit: Truyền Class SavingDeposit lên để lớp cha sử dụng làm Factory,
        #    giúp tự động cắt chuỗi và khởi tạo object Sổ tiết kiệm khi load_data.
        super().__init__('data/savings.txt', SavingDeposit)