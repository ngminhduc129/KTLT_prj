from datetime import datetime, date
class Account:
    def __init__(self, account_id, full_name, balance, pin, user_id, password, status, create_at, time_created=None):
        self.account_id = account_id
        self.full_name = full_name
        self.balance = float(balance)
        self.pin = pin
        self.user_id = user_id
        self.password = password
        self.status = status
        self.create_at = create_at

        # Nếu load từ file, lấy thời gian cũ. Nếu tạo mới, lấy thời gian hiện tại.
        if time_created:
            self.time_created = time_created
        else:
            self.time_created = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Kiểm tra mã pin
    def check_pin(self, pin):
        return self.pin == pin
    
    # Kiểm tra mật khẩu khi đăng nhập vào tài khoản
    def check_password(self, password):
        return self.password == password
    
    # In ra 
    def display_info(self):
        print("Số tài khoản: ", self.account_id)
        print("Tên chủ tài khoản: ", self.full_name)
        print("Số dư tài khoản: ", self.balance)
        print("Trạng thái: ", self.status)
        print("Chi nhánh: ", self.create_at)
        print("Ngày mở tài khoản: ", self.time_created)
    
    # Nối các thuộc tính từ tham số đầu vào thành một chuỗi
    def to_file_string(self):
        return f"{self.account_id}|{self.full_name}|{self.balance}|{self.pin}|{self.user_id}|{self.password}|{self.status}|{self.create_at}|{self.time_created}"
    
    # Khi thực hiện một chức năng load data từ file text ta sẽ tách các thuộc tính ra riêng biệt
    @staticmethod
    def from_file_string(line):
        data = line.strip().split('|')
        return Account(
            account_id=data[0],
            full_name=data[1],
            balance=data[2],
            pin=data[3],
            user_id=data[4],
            password=data[5],
            status=data[6],
            create_at=data[7],
            time_created=data[8]           
        )
