from Services.user_service import UserService
from Services.account_service import AccountService
from Services.saving_service import SavingService
from Models.user import User
from Models.account import Account
from Models.saving_deposit import SavingDeposit
from Models.transaction import Transaction
from datetime import datetime
class BankService:
    def __init__(self):
        self.user_service = UserService()
        self.account_service = AccountService()
        self.saving_service = SavingService()

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
            new_account = self.account_service.create_account(
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
        accounts = self.account_service.get_accounts_by_user_id(user_id)
        """Because we've already checked if the user ID is already in the Users list, 
        we don't need to check len(accounts) again at this step.""" 
        print("\nAvailable Account IDs:")
        current = accounts.head
        while current:
            account: Account = current.value
            print(account.account_id)
            current = current.next

        account_id = input("Account ID: ")

        password = input("Password: ")

        # Enter the amount of money that you wanna deposit into this account
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
                amount,
                password
            )

            print("\nDeposit successfully!")

            updated_account.display_info()

        except ValueError as e:

            print(e)

        # Add transaction " Cho ban NMD"
        
    def withdraw_money(self):
        """
        Withdraw by QR
        """
        # Need to log in your bank account mobile
        print("Please enter the necessary information to withdraw money into your bank account.")

        user_id = input("User ID: ")
        # Check if the citizen identification card exists
        try:
            user = self.user_service.find_user_by_id(user_id)
            print("\nUser Information: ")
            user.display_info()
        except ValueError as e:
            print(e)
            return
        
        # Display all bank accounts have the same user id and we will choose one of them to withdraw
        accounts = self.account_service.get_accounts_by_user_id(user_id)
        """Because we've already checked if the user ID is already in the Users list, 
        we don't need to check len(accounts) again at this step.""" 
        print("\nAvailable Account IDs:")
        current = accounts.head
        while current:
            account: Account = current.value
            print(account.account_id)
            current = current.next

        account_id = input("Account ID: ")

        password = input("Password: ")

        # Enter the amount of money that you wanna withdraw 
        try:
            amount = float(input("Enter the amount you want to withdraw."))
        except ValueError:
            print("Invalid amount!")
            return

        # Confirm and deposit
        pin = input("PIN: ")
        try:
            # Withdraw
            update_account = self.account_service.withdraw(
                account_id,
                pin,
                amount,
                password
            )
            print("\nWithdraw successfully!")
            update_account.display_info()
        except ValueError as e:
            print(e)
        
        # Add transaction
    # Add transaction
    def transfer_money(self):
        # Information of source account
        # Log in
        print("Please enter the neccessary information to transfer money from a from_account bank")
        user_id_from = input("User ID of the source account: ")
        
        # check user_id
        try:
            user_source = self.user_service.find_user_by_id(user_id_from)
            print("\nUser information of source account: ")
            user_source.display_info()
        except ValueError as e:
            print(e)
            return
        
        # Display all bank accounts are common on this user id source
        accounts = self.account_service.get_accounts_by_user_id(user_id_from)

        while accounts.head is None:
            print("This user has no bank accounts")
            return

        print("\nList of bank accounts: ")
        current = accounts.head
        while current:
            account: Account = current.value
            print(account.account_id)
            current = current.next

        account_id_source = input("Account ID of source account")

        password = input("Password of source account: ")

        # Enter the amount of money that you want to transfer money to a bank account
        try:
            amount = float(input("Enter the amount you want to transfer: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                return
        except ValueError:
            print("Invalid amount!")
            return

        pin = input("Pin of source account: ")

        # Information of the target account id 
        account_id_target = input("Account ID of targer account: ")

        # Transfer
        try:
            updated_account_source, updated_account_target = self.account_service.transfer(
                account_id_source,
                account_id_target,
                amount,
                pin,
                password
            )

            print("Transfer Successfully!")
            print("\nUpdated source account:")
            updated_account_source.display_info()

            print("\nUpdated target account:")
            updated_account_target.display_info()
        except ValueError as e:
            print(e)

        # Add transaction...

    def create_saving(self):
        print("Please enter some neccessary infromation to create your saving account")

        # Information
        saving_id = self.saving_service.generate_saving_id()
        print("Saving ID:", saving_id)
        owner_account_id = input("Owner Account ID: ") # Bank account: will need when customer want to close the saving account
        amount = float(input("Amount to send: "))
        # start_date is None because in SavingDeposit, I created a function to get the real time
        start_date = None

        # Create a saving account
        try:
            new_saving = self.saving_service.create_saving(
                saving_id,
                owner_account_id,
                amount, 
                start_date
            )
            print("Create a saving account successfully!")
            new_saving.display_info()
        except ValueError as e:
            print(e)


    def withdraw_interest(self):
        print("Please enter some neccessary information of your saving account")

        # Information
        saving_id = input("Saving Account ID: ")
        
        try:
            saving_account = self.saving_service.find_saving_account(saving_id)
            saving_account.display_info()
        except ValueError as e:
            print(e)
            return
        
        # Get bank account to transfer interest to it
        account_id = saving_account.owner_account_id

        # Calculate interest
        interest = self.saving_service.calculate_interest(saving_id)

        # Deposit money into the original bank account
        print("Please enter some neccessary infromation to log in your bank account")
        password = input("Password: ")
        pin = input("Pin: ")
        try:
            account = self.account_service.deposit(account_id, pin, interest, password)
            print("Deposit successfully!")
            account.display_info()
        except ValueError as e:
            print(e)

        # Update maturity date
        saving_account.maturity_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("Update successfully!")

    def close_saving_account(self):
        print("Please enter some neccessary information of your saving account to close")
        
        # Information
        saving_id = input("Saving Account ID: ")
        
        # Find saving_id to get some information so that the system can get all money(original, interest) into users'bank account
        try:
            saving_account = self.saving_service.find_saving_account(saving_id)
            saving_account.display_info()
        except ValueError as e:
            print(e)
            return
        
        # Finalize the settlement
        final_receieved_money = saving_account.amount + self.saving_service.calculate_interest(saving_id)
        print("Please enter some neccessary infromation to log in your bank account")
        password = input("Password: ")
        pin = input("Pin: ")
        try:
            account = self.account_service.deposit(saving_account.owner_account_id, pin, final_receieved_money , password)
            print("Deposit successfully!")
            account.display_info()
        except ValueError as e:
            print(e)

        # Add transaction

        # Close saving account
        try:
            saving = self.saving_service.close_saving(saving_id)
            print("Close saving account successfully!")
            saving.display_info()
        except ValueError as e:
            print(e)
        
    def show_statement(self):
        pass

    