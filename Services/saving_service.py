from Structures.Hash_table import Hash_table
from Structures.Linked_list import LinkedList
from Models.saving_deposit import SavingDeposit
from Services.account_service import AccountService
from datetime import datetime
class SavingService:
    def __init__(self, account_service=None):
        self.saving_storage = Hash_table()
        self.account_service = account_service

    def create_saving(
            self, 
            saving_id: str,
            owner_account_id: str,
            amount: float,
            start_date: str) -> SavingDeposit:
        """
        Create a new saving deposit with a random generated saving_id and given parameters
        Raises:
            ValuerError: If saving_id already exists
        """
        if self.saving_storage.search(saving_id) is not None:
            raise ValueError(f"Saving deposit {saving_id} already exists")
        try:
            # account_service = AccountService()
            # account = account_service.account_storage.search(owner_account_id)
            account = self.account_service.find_account(owner_account_id)
            # if account is None:
            #     raise ValueError(f"Account {owner_account_id} does not exist")
            full_name = account.full_name
            user_id = account.user_id
        except ValueError:
            full_name = "Unknown User"
            user_id = "Unknown User"

        term = "NO TERM"

        new_saving = SavingDeposit(
            saving_id, 
            owner_account_id, 
            full_name,
            user_id, 
            amount,
            term,
            start_date,
            maturity_date = None,
            close_date = None,
            status = "ACTIVE"
        )

        # Add a saving deposit into HashTable
        self.saving_storage.insert(new_saving.saving_id, new_saving)

        return new_saving
    
    def get_months_passed(self, start_date):
        # Calculate the number of months between start_date and maturity_date and convert to int
        start = datetime.strptime(start_date, "%d/%m/%Y %H:%M:%S")
        maturity = datetime.now()
        
        months = (maturity.year - start.year) * 12 + (maturity.month - start.month) 
        if maturity.day < start.day:
            months -= 1

        return months

    def calculate_interest(self, saving_id):
        # Find your saving deposit
        saving = self.saving_storage.search(saving_id)
        if saving is None:
            raise ValueError(f"Saving account {saving_id} does not exits")

        # calculating the number of months that users deposit savings
        if saving.maturity_date is None:
            final_settlement_date = saving.start_date
        else:
            final_settlement_date = saving.maturity_date
        months = self.get_months_passed(final_settlement_date)
        amount = saving.amount

        # Set up interest rate = 0.2%/month
        interest_rate = 0.002
        # Total interest for months
        interest = amount * interest_rate * months

        return interest
    
    def close_saving(self, saving_id) -> SavingDeposit:
        saving = self.saving_storage.search(saving_id)
        if saving is None:
            raise ValueError(f"Saving account {saving_id} does not exists")
        # Update status of saving from Active to Invalid
        saving.status = "Invalid"
        saving.close_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        saving.amount = 0
        return saving
    
    def get_users_saving(self):
        users_saving = LinkedList()
        for bucket in self.saving_storage.table:
            current = bucket
            while current is not None:
                user = current.value
                users_saving.append(current.key, user)
                current = current.next   
        return users_saving
                
    def get_active_savings(self):
        active_savings = LinkedList()
        for bucket in self.saving_storage.table:
            current = bucket
            while current is not None:
                active = current.value
                if active.status == "ACTIVE":
                    active_savings.append(current.key, active)
                current = current.next
        return active_savings

    def generate_saving_id(self):
        # Generate a random saving deposit id with format "STK" + 6 digits
        import random
        while True:
            saving_id = "STK" + str(random.randint(000000, 999999)).zfill(6)
            if self.saving_storage.search(saving_id) is None:
                return saving_id

    def find_saving_account(self, saving_id: str) -> SavingDeposit:
        """
        Find and return a saving account by saving_id

        Raise:
            ValuerError: if the saving account does not exist
        """
        saving_account = self.saving_storage.search(saving_id)
        
        if saving_account is None:
            raise ValueError(f"Saving Account with {saving_id} does not exist")
        return saving_account
    
    def get_all_savings(self):
        return self.saving_storage.values()