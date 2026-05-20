from Structures.Hash_table import Hash_table
from Structures.Linked_list import LinkedList
from Models.saving_deposit import SavingDeposit
from Services.account_service import AccountService
from datetime import datetime
class SavingService:
    def __init__(self):
        self.saving_storage = Hash_table()

    def create_saving(
            self, 
            deposit_id: str,
            owner_account_id: str,
            amount: float,
            interest_rate: float,
            term: int,
            start_date: str) -> SavingDeposit:
        """
        Create a new saving deposit with a random generated deposit_id and given parameters
        Raises:
            ValuerError: If deposit_id already exists
        """
        if self.saving_storage.search(deposit_id) is not None:
            raise ValueError(f"Saving deposit {deposit_id} already exists")
        try:
            account_service = AccountService()
            account = account_service.account_storage.search(owner_account_id)
            if account is None:
                raise ValueError(f"Account {owner_account_id} does not exist")
            full_name = account.full_name
            user_id = account.user_id
        except ValueError:
            full_name = "Unknown User"
            user_id = "Unknown User"
        
        new_saving = SavingDeposit(
            deposit_id, 
            owner_account_id, 
            full_name,
            user_id, 
            amount,
            interest_rate,
            term,
            start_date,
            maturity_date = None,
            status = "Active"
        )

        # Add a saving deposit into HashTable
        self.saving_storage.insert(new_saving)

        return new_saving
    
    def get_months_passed(self, start_date):
        # Calculate the number of months between start_date and maturity_date and convert to int
        start = datetime.strptime(start_date, "%d/%m/%Y %H:%M:%S")
        maturity = datetime.now()
        
        months = (maturity.year - start.year) * 12 + (maturity.month - start.month) 
        if months < start.day:
            months -= -1

        return months

    def calculate_interest(self, deposit_id) -> SavingDeposit:
        # Find your saving deposit
        saving = self.saving_storage.search(deposit_id)
        if saving is None:
            raise ValueError(f"Saving account {deposit_id} does not exits")

        # calculating the number of months that users deposit savings
        months = self.get_months_passed(saving.start_date)
        amount = saving.amount
        interest_rate = saving.interest_rate
        # Total interest for months
        interest = amount * interest_rate * months

        return interest
    
    def close_saving(self, deposit_id):
        saving = self.saving_storage.search(deposit_id)
        if saving is None:
            raise ValueError(f"Saving account {deposit_id} does not exists")
        # Update status of saving from Active to Invalid
        saving.status = "Invalid"
        saving.maturity_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return saving
    
    def get_users_saving(self):
        users_saving = LinkedList()
        for bucket in self.saving_storage.table:
            current = bucket
            while current is not None:
                user = current.value
                users_saving.append(user)
                current.next   
        return users_saving
                
    def get_active_savings(self):
        active_savings = LinkedList()
        for bucket in self.saving_storage.table:
            current = bucket
            while current is not None:
                active = current.value
                if active.status == "Active":
                    active_savings.append(active)
                current.next
        return active_savings

    def generate_saving_id(self):
        # Generate a random saving deposit id with format "STK" + 6 digits
        import random
        while True:
            deposit_id = "STK" + str(random.randint(000000, 999999)).zfill(6)
            if self.saving_storage.search(deposit_id) is None:
                return deposit_id