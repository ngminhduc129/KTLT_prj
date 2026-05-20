from Structures.Hash_table import Hash_table
from Models.account import Account
from Services.user_service import UserService

class AccountService:
    """
    Service layer for managing bank accounts.
    This class handles all business logic related to accounts.
    """

    def __init__(self):
        self.account_storage = Hash_table()


    def create_account(self, account_id: str, password: str,
                        user_id: str, pin: str, create_at: str) -> Account:
        """
        Create a new account.
        
        Raises:
            ValueError: If account_id already exists
        """
        if self.account_storage.search(account_id):
            raise ValueError(f"Account {account_id} already exists")
        
        try:
            user_service = UserService()                    
            user = user_service.find_user_by_id(user_id)
            full_name = user.full_name
        except ValueError:
            full_name = "Unknown User"

        new_account = Account(account_id, 
                              full_name, 
                              balance = 0.0, 
                              pin = pin, 
                              user_id = user_id, 
                              password = password, 
                              status = "Active", 
                              create_at = create_at, 
                              time_created=None  )
        
        self.account_storage.insert(new_account)   # Adjust if your HashTable needs key-value

        return new_account


    def authenticate(self, account_id: str, password: str) -> Account:
        """
        Authenticate user with account ID and password.
        
        Raises:
            ValueError: If account doesn't exist or password is wrong
        """
        account = self.account_storage.search(account_id)
        
        if not account:
            raise ValueError(f"Account {account_id} does not exist")
        
        if account.password != password:
            raise ValueError("Invalid password")
        
        return account


    def deposit(self, account_id: str, pin: str, amount: float) -> Account:
        """
        Deposit money into an account.
        
        Raises:
            ValueError: If amount is invalid, account not found, or PIN is wrong
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than 0")

        account = self.account_storage.search(account_id)
        if account is None:
            raise ValueError(f"Account {account_id} does not exist")

        if account.pin != pin:
            raise ValueError("Invalid PIN")

        account.balance += amount
        
        return account
    

    def withdraw(self, account_id: str, pin: str, amount: float) -> Account:
        '''
        Withdraw money from an account

        Raises:
            ValueError: If amount > balance, account_id not found, PIN is wrong
        '''

        account = self.account_storage.search(account_id)
        
        if account is None:
            raise ValueError(f"Account {account_id} does not exist")
        
        if account.pin != pin:
            raise ValueError("Invalid PIN")
        
        balance = account.balance

        if amount <= 0:
            raise ValueError("Withdraw amount must be greater than 0")

        if amount > balance:
            raise ValueError("Withdraw amount must be less than balance")
        
        account.balance -= amount
        
        return account
    

    def transfer(self, source_account_id: str, target_account_id: str, 
                 amount: float, pin: str):
        '''
        Transfer money from source account to target account.
        
        Returns:
            tuple: (source_account, target_account) after transfer success
        '''

        if amount <= 0:
            raise ValueError("Transfer amount must be greater than 0")
        
        source = self.account_storage.search(source_account_id)

        if source is None:
            raise ValueError(f"Source account {source_account_id} does not exist")
        
        if source.pin != pin:
            raise ValueError("Invalid PIN")

        if amount > source.balance:
            raise ValueError("Transfer amount must less than balance")
        
        if source_account_id == target_account_id:
            raise ValueError("Cannot transfer to the same account")
        
        target = self.account_storage.search(target_account_id)
        if target is None:
            raise ValueError(f"Target account {target_account_id} does not exist")

        source.balance -= amount
        target.balance += amount

        return source, target
    
    def find_account(self, account_id: str) -> Account:
        """
        Find and return an account by account_id.
        
        Raises:
            ValueError: If account does not exist
        """
        account = self.account_storage.search(account_id)
        
        if account is None:
            raise ValueError(f"Account {account_id} does not exist")
        
        return account
    

    def display_all_accounts(self):
        """Display information of all account (for console/debug)"""
        is_empty = True
        
        for bucket in self.account_storage.table:
            current = bucket

            while current:
                account = current.value
                account.display_info()
                current = current.next
                is_empty = False

        if is_empty:
            print("No users found")


    def change_pin(self, account_id: str, password: str, old_pin: str, new_pin: str) -> Account:
        '''
        Change pin require account id , password, old pin, new pin
        Return : Account
        '''

        account = self.account_storage.search(account_id)
        
        if account is None:
            raise ValueError(f"Account {account_id} does not exist")
        
        if account.password != password:
            raise ValueError("Invalid password")
        
        if account.pin != old_pin:
            raise ValueError("Invalid pin")

        account.pin = new_pin

        return account


    def unlock_account(self, account_id: str, password: str, pin: str) -> Account:
        '''
        Unlock account require account id , password, pin
        Return : Account
        '''        

        account = self.account_storage.search(account_id)
        
        if account is None:
            raise ValueError(f"Account {account_id} does not exist")
        
        if account.password != password:
            raise ValueError("Invalid password")
        
        if account.pin != pin:
            raise ValueError("Invalid pin")

        if account.status == "Unlock":
            raise ValueError("The account is already unlock")

        account.status = "Unlock"

        return account
    

    def lock_account(self, account_id: str, password: str, pin: str) -> Account:
        '''
        lock account require account id , password, pin
        Return : Account
        '''        

        account = self.account_storage.search(account_id)
        
        if account is None:
            raise ValueError(f"Account {account_id} does not exist")
        
        if account.password != password:
            raise ValueError("Invalid password")
        
        if account.pin != pin:
            raise ValueError("Invalid pin")

        if account.status == "Lock":
            raise ValueError("The account is already Lock")

        account.status = "Lock"

        return account

