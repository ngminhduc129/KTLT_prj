from datetime import datetime, date
class SavingDeposit:
    def __init__(
            self, 
            saving_id, 
            owner_account_id, 
            full_name,
            user_id,
            amount, 
            term, 
            start_date,
            maturity_date,
            close_date,
            status
        ):
            self.saving_id = saving_id
            self.owner_account_id = owner_account_id
            self.full_name = full_name
            self.user_id = user_id
            self.amount = float(amount)
            self.term = term
            self.start_date = (start_date or datetime.now().strftime("%d/%m/%Y %H:%M:%S") )
            self.maturity_date = maturity_date 
            self.close_date = close_date
            self.status = status
    
    def display_info(self):
        print("Saving Account ID: ", self.saving_id)
        print("Owner Account ID: ", self.owner_account_id)
        print("Full name: ", self.full_name)
        print("User ID: ", self.user_id)
        print("Amount: ", self.amount)
        print("Term: ", self.term)
        print("Start date ", self.start_date)
        print("Maturity date: ", self.maturity_date)
        print("Close date: ", self.close_date)
        print("Status: ", self.status)

    def to_file_string(self):
        return f"{self.saving_id}|{self.owner_account_id}|{self.full_name}|{self.user_id}|{self.amount}|{self.term}|{self.start_date}|{self.maturity_date}|{self.close_date}|{self.status}"
    
    @staticmethod
    def from_file_string(line):
        data = line.strip().split('|')
        return SavingDeposit(
            saving_id=data[0],
            owner_account_id=data[1],
            full_name=data[2],
            user_id=data[3],
            amount=data[4],
            term=data[5],
            start_date=data[6],
            maturity_date=data[7],
            close_date=data[8],
            status=data[9]
        )