from datetime import datetime, date
class Transaction:
    def __init__(
            self, 
            trans_id: str, 
            from_account: str, 
            to_account: str, 
            type_trans: str, 
            amount: float, 
            timestamp: str, 
            description: str, 
            balance_after: float
        ):
            self.trans_id = trans_id
            self.from_account = from_account
            self.to_account = to_account
            self.type_trans = type_trans
            self.amount = amount
            self.timestamp = timestamp
            self.description = description
            self.balance_after = balance_after

            if timestamp:
                self.timestamp = timestamp
            else:
                self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def display_info(self):
        print("ID giao dịch: ", self.trans_id)
        print("Tài khoản nguồn: ", self.from_account)
        print("Tài khoản đích: ", self.to_account)
        print("Loại giao dịch: ", self.type_trans)
        print("Số tiền: ", self.amount)
        print("Thời gian: ", self.timestamp)
        print("Mô tả: ", self.description)
        print("Số dư sau giao dịch: ", self.balance_after)
    
    def to_file_string(self):
         return f"{self.trans_id}|{self.from_account}|{self.to_account}|{self.type_trans}|{self.amount}|{self.timestamp}|{self.description}|{self.balance_after}"
    
    @staticmethod
    def from_file_string(line):
         data = line.strip().split('|')
         return Transaction(
             trans_id=data[0],
             from_account=data[1],
             to_account=data[2],
             type_trans=data[3],
             amount=float(data[4]),
             timestamp=data[5],
             description=data[6],
             balance_after=float(data[7])
         )
