from Structures.Hash_table import Hash_table
from Models.user import User

class UserService:
    def __init__(self):
        self.user_storage = Hash_table()

    def create_user(self, user_id, full_name, phone, email, sex, address, job, dob):
        if self.user_storage.search(user_id):
            print(f"Already exist user {user_id}")
            return None

        new_user = User(user_id, full_name, phone, email, sex, address, job, dob)
    
        self.user_storage.insert(user_id, new_user)

        print("Create account successfully!")
        return new_user
    
    def update_user(self, user_id, full_name = None, phone = None, email = None, sex = None, address = None, job = None, dob = None):
        user_change : User = self.user_storage.search(user_id)

        if user_change is None:
            print("User not found")
            return False
        
        if full_name is not None:
            user_change.full_name = full_name

        if phone is not None:
            user_change.phone = phone

        if email is not None:
            user_change.email = email

        if sex is not None:
            user_change.sex = sex

        if address is not None:
            user_change.address = address

        if job is not None:
            user_change.job = job

        if dob is not None:
            user_change.dob = dob

        print("Update successfully")
        return True
    
if __name__ == "__main__":

    service = UserService()

    service.create_user(
        "001",
        "Nguyen Minh Duc",
        "0123456789",
        "duc@gmail.com",
        "Male",
        "Ha Noi",
        "Student",
        "2005-01-01"
    )

    service.update_user(
        "001",
        full_name="Duc đẹp trai"
    )

    user = service.user_storage.search("001")

    print(user.full_name)