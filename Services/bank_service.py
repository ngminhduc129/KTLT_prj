from Services.user_service import UserService
from Services.account_service import AccountService
from Services.saving_service import SavingService
from Services.transaction_service import TransactionService
from Models.user import User
from Models.account import Account
from Models.saving_deposit import SavingDeposit
from Models.transaction import Transaction
from datetime import datetime
from Persistence.User_repository import User_repository
from Persistence.Account_repository import Account_repository
from Persistence.Saving_repository import Saving_repository
from Persistence.Transaction_repository import Transaction_repository


class BankService:
    def __init__(self):
        self.user_service = UserService()
        self.account_service = AccountService(self.user_service)
        self.saving_service = SavingService(self.account_service)
        self.transaction_service = TransactionService()

    def create_customer_and_account(self, user_id, full_name, phone, email,
                                     sex, address, job, dob,
                                     password, pin, branch):
        
        if not phone or not phone.isdigit():
            raise ValueError("Phone must be all numbers.")
        if len(phone) != 10:
            raise ValueError("Phone must have 10 numbers.")
        
        self.user_service.validate_email(email)

        special_chars = "!@#$%^&*()-_=+[]{}|;:',.<>?/"
        if not password:
            raise ValueError("Password is empty.")
        if not password[0].isupper():
            raise ValueError("Password must have the first uppercase letter.")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one number.")
        if not any(c in special_chars for c in password):
            raise ValueError("Password must contain at least one special character.")

        if not pin or not pin.isdigit():
            raise ValueError("PIN must be all numbers.")
        
        count = 0
        for c in pin:
            count += 1
        
        if count != 6:
            raise ValueError("PIN must have 6 enough numbers.")

        user = self.user_service.create_user(
            user_id, full_name, phone, email, sex, address, job, dob
        )

        account_id = self.account_service.generate_account_id()
        account = self.account_service.create_account(
            account_id, password, user_id, pin, branch
        )
        return user, account

    def create_account(self, user_id, password, pin, branch):

        self.user_service.find_user_by_id(user_id)

        special_chars = "!@#$%^&*()-_=+[]{}|;:',.<>?/"
        if not password:
            raise ValueError("Password is empty.")
        if not password[0].isupper():
            raise ValueError("Password must have the first uppercase letter.")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one number.")
        if not any(c in special_chars for c in password):
            raise ValueError("Password must contain at least one special character.")

        if not pin or not pin.isdigit():
            raise ValueError("PIN must be all numbers.")       


        account_id = self.account_service.generate_account_id()
        account = self.account_service.create_account(
            account_id, password, user_id, pin, branch
        )
        return account

    def deposit_money(self, account_id, amount, pin):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        account = self.account_service.deposit(account_id, pin, amount)
        trans = self.transaction_service.add_transaction(
            from_account=None,
            to_account=account_id,
            type_trans="Deposit",
            amount=amount,
            description=f"Deposit money into {account_id}",
            balance_after=account.balance
        )
        return account, trans

    def withdraw_money(self, account_id, amount, pin):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        account = self.account_service.withdraw(account_id, pin, amount)
        trans = self.transaction_service.add_transaction(
            from_account=account_id,
            to_account=None,
            type_trans="Withdraw",
            amount=amount,
            description=f"Withdraw money from {account_id}",
            balance_after=account.balance
        )
        return account, trans

    def transfer_money(self, src_account, dst_account, amount, pin, password):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        src_acc, dst_acc = self.account_service.transfer(
            src_account, dst_account, amount, pin, password
        )
        self.transaction_service.add_transaction(
            from_account=src_account,
            to_account=dst_account,
            type_trans="Transfer",
            amount=amount,
            description=f"Transfer from {src_account} to {dst_account}",
            balance_after=src_acc.balance
        )
        self.transaction_service.add_transaction(
            from_account=src_account,
            to_account=dst_account,
            type_trans="Receive",
            amount=amount,
            description=f"Receive from {src_account}",
            balance_after=dst_acc.balance
        )
        return src_acc, dst_acc

    def create_saving(self, owner_account_id, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        saving_id = self.saving_service.generate_saving_id()
        saving = self.saving_service.create_saving(
            saving_id, owner_account_id, amount, None
        )
        return saving

    def withdraw_interest(self, saving_id, pin):
        saving_account = self.saving_service.find_saving_account(saving_id)
        account_id = saving_account.owner_account_id
        interest = self.saving_service.calculate_interest(saving_id)

        account = self.account_service.deposit(account_id, pin, interest)
        trans = self.transaction_service.add_transaction(
            from_account=None,
            to_account=account_id,
            type_trans="Interest",
            amount=interest,
            description="Bank transfer interest",
            balance_after=account.balance
        )

        saving_account.maturity_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return account, interest

    def close_saving_account(self, saving_id, password, pin):
        saving_account = self.saving_service.find_saving_account(saving_id)
        interest = self.saving_service.calculate_interest(saving_id)
        total = saving_account.amount + interest

        account = self.account_service.deposit(
            saving_account.owner_account_id, pin, total
        )
        trans = self.transaction_service.add_transaction(
            from_account=None,
            to_account=saving_account.owner_account_id,
            type_trans="Settlement Saving Account",
            amount=total,
            description="The bank closed the savings account",
            balance_after=account.balance
        )

        self.saving_service.close_saving(saving_id)
        return account, total

    def save_all_data(self):
        User_repository().save_data(
            self.user_service.get_all_users()
        )

        Account_repository().save_data(
            self.account_service.get_all_accounts()
        )

        Saving_repository().save_data(
            self.saving_service.get_all_savings()
        )

        Transaction_repository().save_data(
            self.transaction_service.get_all_transactions()
        )

    def load_all_data(self):
        import os
        data_files = ['data/users.txt', 'data/accounts.txt', 'data/transactions.txt', 'data/savings.txt']
        for f in data_files:
            if not os.path.exists(f):
                os.makedirs(os.path.dirname(f), exist_ok=True)
                open(f, 'a', encoding='utf-8').close()

        user_repo = User_repository()
        users = user_repo.load_data()
        while users.head is not None:
            user: User = users.head.value
            self.user_service.user_storage.insert(
                user.user_id,
                user
            )
            users.head = users.head.next

        account_repo = Account_repository()
        accounts = account_repo.load_data()
        while accounts.head is not None:
            account: Account = accounts.head.value
            self.account_service.account_storage.insert(
                account.account_id,
                account
            )
            accounts.head = accounts.head.next

        saving_repo = Saving_repository()
        savings = saving_repo.load_data()
        while savings.head is not None:
            saving: SavingDeposit = savings.head.value
            self.saving_service.saving_storage.insert(
                saving.saving_id,
                saving
            )
            savings.head = savings.head.next

        trans_repo = Transaction_repository()
        transactions = trans_repo.load_data()
        current = transactions.head
        while current is not None:
            transaction: Transaction = current.value
            self.transaction_service.trans_storage.append(
                transaction.trans_id,
                transaction
            )
            current = current.next
