from datetime import datetime, date
class SavingDeposit:
    def __init__(
            self, 
            deposit_id, 
            owner_account_id, 
            full_name,
            user_id,
            amount, 
            interest_rate, 
            term, 
            start_date, 
            maturity_date, 
            status
        ):
            self.deposit_id = deposit_id
            self.owner_account_id = owner_account_id
            self.full_name = full_name
            self.user_id = user_id
            self.amount = amount
            self.interest_rate = interest_rate
            self.term = term
            self.start_date = start_date
            self.maturity_date = maturity_date
            self.status = status

            if self.start_date:
                self.start_date = start_date
            else:
                self.start_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def display_info(self):
        print("ID sổ tiết: ", self.deposit_id)
        print("Số tài khoản chủ số: ", self.owner_account_id)
        print("Tên chủ số: ", self.full_name)
        print("Giấy tờ tùy thân: ", self.user_id)
        print("Số tiền gửi: ", self.amount)
        print("Lãi suất: ", self.interest_rate)
        print("Kỳ hạn: ", self.term)
        print("Ngày bắt đầu gửi: ", self.start_date)
        print("Ngày đáo hạn: ", self.maturity_date)
        print("Trạng thái: ", self.status)

    def to_file_string(self):
        return f"{self.deposit_id}|{self.owner_account_id}|{self.full_name}|{self.user_id}|{self.amount}|{self.interest_rate}|{self.term}|{self.start_date}|{self.maturity_date}|{self.status}"
    
    @staticmethod
    def from_file_string(line):
        data = line.strip().split('|')
        return SavingDeposit(
            deposit_id=data[0],
            owner_account_id=data[1],
            full_name=data[2],
            user_id=data[3],
            amount=data[4],
            interest_rate=data[5],
            term=data[6],
            start_date=data[7],
            maturity_date=data[8],
            status=data[9]
        )