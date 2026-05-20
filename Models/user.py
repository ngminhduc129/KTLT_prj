class User:
    def __init__(self, user_id, full_name, phone, email, sex, address, job, dob):
        self.user_id = user_id
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.sex = sex
        self.address = address
        self.job = job
        self.dob = dob

    def display_info(self):
        print("Giấy tờ tùy thân: ", self.user_id)
        print("Họ và tên: ", self.full_name)
        print("Số điện thoại: ", self.phone)
        print("Email: ", self.email)
        print("Giới tính: ", self.sex)
        print("Địa chỉ: ", self.address)
        print("Nghề nghiệp: ", self.job)
        print("Ngày sinh: ", self.dob)
        
    def to_file_string(self):
        return f"{self.user_id}|{self.full_name}|{self.phone}|{self.email}|{self.sex}|{self.address}|{self.job}|{self.dob}"
    
    @staticmethod
    def from_file_string(line):
        data = line.strip().split('|')
        return User(
            user_id=data[0],
            full_name=data[1],
            phone=data[2],
            email=data[3],
            sex=data[4],
            address=data[5],
            job=data[6],
            dob=data[7]
        )
    