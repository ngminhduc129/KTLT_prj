from Services.user_service import UserService
from Services.account_service import AccountService
from Services.saving_service import SavingDeposit
from Models.user import User
from Models.account import Account
from Models.saving_deposit import SavingDeposit
from Models.transaction import Transaction
class BankService:
    def __init__(self):
        self.user_service = UserService()
        self.accout_service = AccountService()
        self.saving_service = SavingDeposit()

    def create_customer_and_account(self):
        print("Please to import some useful information")
        # Information for create user in UserService()
        user_id = input("User ID: ")
        full_name = input("Full name: ")
        phone = input("Phone: ")
        email = input("Email: ")
        sex = input("Sex: ")
        address = input("Address: ")
        job = input("Job: ")
        dob = input("Birth day: ")
        user = UserService(
            user_id,
            full_name,
            phone,
            email,
            sex,
            address,
            job,
            dob
        )
        # Create user
        try:
            new_user = self.user_service.create_user(
                user_id,
                full_name,
                phone,
                email,
                sex,
                address,
                job,
                dob)
            print("Create a user successfully!")
            new_user.display_info()
        except ValueError as e:
            print(e)
            return


        # Information for creating accout in AccountService()
        account_id = input() # Generate random use def generate_account_id from AccountService
        while True:
            password = input("Password: ")
            if not password:
                print("Password is empty. Please import agian!")
                continue
            
            # Check upper
            check_upper = False
            if password[0].isupper():
                check_upper = True
    
            # Check number, special character
            check_number = False
            check_special = False

            special_chars = "!@#$%^&*()-_=+[]{}|;:',.<>?/"
            for i in range(len(password)):
                if password[i].isdigit():
                    check_number = True

                if password[i] in special_chars:
                    check_special = True
            
            if check_upper == True and check_special == True and check_number == True:
                print("Valid password!")
                break
            else:
                print("Password must have the first uppercase letter, a least number and special letter.")

        while True:
            pin = input("Pin: ")
            if not pin:
                print("Pin is empty. Please import agian!")
                continue
            # All of letters in pin must be numbers
            check_pin = True
            for i in range(len(pin)):
                if not pin[i].isdigit():
                    check_pin = False
            if check_pin  == True:
                print("Valid pin!")
                break
            else:
                print("Pin must be all numbers")
        
        create_at = input("Bank branch: ")

        # Create a account 
        try:
            new_account = self.accout_service.create_account(
                account_id,
                password,
                user_id,
                pin,
                create_at
            )
            print("Create a bank account successfully!")
            new_account.display_info()
        except ValueError as e:
            print(e)
            return

    def deposit_money(self):
        print("Please enter the necessary information to deposit money into your bank account.")

        user_id = input("User ID: ")
        # Check if the citizen identification card exists
        try:
            user = self.user_service.find_user_by_id(user_id)
            print("\nUser Information: ")
            user.display_info()
        except ValueError as e:
            print(e)
            return
        
        # Display all bank accounts have the same user id and we will choose one of them to deposit
        accounts = self.accout_service.get_accounts_by_user_id(user_id)
        """Because we've already checked if the user ID is already in the Users list, 
        we don't need to check len(accounts) again at this step.""" 
        print("\nAvailable Account IDs:")
        current = accounts.head
        while current:
            account = current.value
            print(account.account_id)
            current = current.next

        account_id = input("Account ID: ")

        # Check account_id is correct????
        try:
            account = self.account_service.find_account(account_id)
            account.display_info()
        except ValueError as e:
            print(e)
            return

        password = input("Password: ")
        # Check password of this account
        if not account.check_password(password):
            print("Password is incorrect!")
            return
        print("Valid password!")

        # Enter the amount of money that you wanna deposit into this accout
        try:
            amount = float(input("Enter the amount you want to deposit."))
        except ValueError:
            print("Invalid amount!")
            return

        # Confirm and deposit
        pin = input("PIN: ")
        try:

            updated_account = self.account_service.deposit(
                account_id,
                pin,
                amount
            )

            print("\nDeposit successfully!")

            updated_account.display_info()

        except ValueError as e:

            print(e)

        # Add transaction " Cho ban NMD"
        

    def withdraw_money():
        pass

    def transfer_money():
        pass

    def create_saving(self):
        pass


    def show_statement():
        pass

    