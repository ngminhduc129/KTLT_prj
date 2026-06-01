from Structures.Hash_table import Hash_table
from Models.user import User
import re

class UserService:
    """
    Service layer for managing users.
    Handles all user-related business logic.
    """

    def __init__(self):
        self.user_storage = Hash_table()

    def create_user(self, user_id: str, full_name: str, phone: str, email: str,
                   sex: str, address: str, job: str, dob: str) -> User:
        """
        Create a new user.
        
        Raises:
            ValueError: If user_id already exists
        """
        if self.user_storage.search(user_id):
            raise ValueError(f"User with ID {user_id} already exists")

        new_user = User(user_id, full_name, phone, email, sex, address, job, dob)
        
        self.user_storage.insert(new_user.user_id, new_user)

        return new_user

    def update_user(self, user_id: str, full_name=None, phone=None, email=None,
                   sex=None, address=None, job=None, dob=None) -> User:
        """
        Update user information. Only fields with values will be updated.
        
        Raises:
            ValueError: If user is not found
        """
        user = self.user_storage.search(user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")

        if full_name is not None:
            user.full_name = full_name
        if phone is not None:
            user.phone = phone
        if email is not None:
            user.email = email
        if sex is not None:
            user.sex = sex
        if address is not None:
            user.address = address
        if job is not None:
            user.job = job
        if dob is not None:
            user.dob = dob

        return user

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user by user_id.
        
        Raises:
            ValueError: If user does not exist
        """
        if self.user_storage.search(user_id) is None:
            raise ValueError(f"User {user_id} not found")

        self.user_storage.remove(user_id)
        return True

    def find_user_by_id(self, user_id: str) -> User:
        """
        Find user by ID.
        
        Raises:
            ValueError: If user is not found
        """
        user = self.user_storage.search(user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")
        
        return user

    def display_all_users(self):
        """Display information of all users (for console/debug)"""
        is_empty = True
        
        for bucket in self.user_storage.table:
            current = bucket
            while current:
                user = current.value
                user.display_info()
                current = current.next
                is_empty = False

        if is_empty:
            print("No users found")
    
    def get_all_users(self):
        return self.user_storage.values()
    
    def validate_email(self, email):
        if not email:
            raise ValueError("Email cannot be empty.")

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if not re.fullmatch(email_regex, email):
            raise ValueError("Invalid email format.")
            
        return True