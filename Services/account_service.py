from Structures.Hash_table import Hash_table
from Models.account import Account
from Structures.Linked_list import LinkedList

class AccountService:
    """
    Service layer for managing bank accounts.
    This class handles all business logic related to accounts.
    """

    def __init__(self, user_service=None):
        self.account_storage = Hash_table()
        self.user_service = user_service


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
            user = self.user_service.find_user_by_id(user_id)
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
        
        self.account_storage.insert(new_account.account_id, new_account)   # Adjust if your HashTable needs key-value

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

        if account.status == "Lock": 
            raise ValueError("Account is locked")

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
        
        if account.status == "Lock": 
            raise ValueError("Account is locked")

        account.balance -= amount
        
        return account
    

    def transfer(self, source_account_id: str, target_account_id: str, 
                 amount: float, pin: str, password: str) -> LinkedList: 
        '''
        Transfer money from source account to target account.
        
        Returns:
           linked list after transfer success
        '''

        if amount <= 0:
            raise ValueError("Transfer amount must be greater than 0")
        
        source = self.account_storage.search(source_account_id)

        if source is None:
            raise ValueError(f"Source account {source_account_id} does not exist")
        
        if source.password != password:
            raise ValueError("Invalid Password")    

        if source.pin != pin:
            raise ValueError("Invalid PIN")

        if amount > source.balance:
            raise ValueError("Transfer amount must less than balance")
        
        if source_account_id == target_account_id:
            raise ValueError("Cannot transfer to the same account")
        
        target = self.account_storage.search(target_account_id)
        if target is None:
            raise ValueError(f"Target account {target_account_id} does not exist")

        if source.status == "Lock":
            raise ValueError("Account is locked")
        source.balance -= amount
        target.balance += amount

        result = LinkedList()
        result.append(source.account_id, source)
        result.append(target.account_id, target)

        return result
    
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

    def get_accounts_by_user_id(self, user_id) -> LinkedList: 
        accounts_of_user_id = LinkedList()
        for bucket in self.account_storage.table:
            current = bucket
            while current is not None:
                account = current.value
                if account.user_id == user_id:
                    accounts_of_user_id.append(account.account_id, account)
                current = current.next
        return accounts_of_user_id

    def get_all_accounts(self):
        return self.account_storage.values()

    def change_pin(self, account_id: str, new_pin: str) -> Account:
        '''
        Change pin require account id
        Return : Account
        '''

        account = self.account_storage.search(account_id)
        
        if account is None:
            raise ValueError(f"Account {account_id} does not exist")
        
        if not new_pin.isdigit():
            raise ValueError(
                "PIN must contain only numbers."
            )
        
        if len(new_pin) != 6:
            raise ValueError(
                "PIN must be exactly 6 digits."
            )
        
        account.pin = new_pin

        return account

    def change_password(self, account_id: str, new_password: str) -> Account:
        account = self.find_account(account_id)

        if account is None:
            raise ValueError(f"Account {account_id} does not exist")
        
        special_chars = "!@#$%^&*()-_=+[]{}|;:',.<>?/"
        if not new_password:
            raise ValueError("Password is empty.")
        if not new_password[0].isupper():
            raise ValueError("Password must have the first uppercase letter.")
        if not any(c.isdigit() for c in new_password):
            raise ValueError("Password must contain at least one number.")
        if not any(c in special_chars for c in new_password):
            raise ValueError("Password must contain at least one special character.")

        account.password = new_password
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

        if account.status == "Active":
            raise ValueError("The account is already active")

        account.status = "Active"

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

    def generate_account_id(self):
        """
        Generate a unique random account ID
        Format: AC + 6 random digits
        Return: str: unique account id
        """
        import random

        while True:
            account_id = "AC" + str(random.randint(0, 999999)).zfill(6)
            if self.account_storage.search(account_id) is None:
                return account_id
