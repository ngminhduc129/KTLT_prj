from Persistence.File_handler import FileHandler
from Structures.Linked_list import LinkedList

class Base_repository:
    """
    Lớp cơ sở quản lý luồng dữ liệu vào/ra (I/O).
    Chịu trách nhiệm duy nhất là giao tiếp với hệ điều hành để đọc/ghi file thô.
    Không chứa bất kỳ logic nghiệp vụ nào liên quan đến User, Account hay Transaction.  
    """
    def __init__(self, file_path, model_class):
        # Khởi tạo đối tượng giao tiếp trực tiếp với hệ điều hành để xử lý file thô
        self.file_handler = FileHandler(file_path)
        # Lưu lại Class được truyền vào (ví dụ: User, Account)
        # để biết cách khởi tạo đối tượng tương ứng lúc đọc dữ liệu.
        self.model_class = model_class

    def load_data(self):
        """
        Đọc văn bản từ file và chuyển thành đối tượng.
        Trả về: Cấu trúc dữ liệu LinkedList chứa các object.
        """
        raw_data = self.file_handler.read_file()
        data_list = LinkedList()
        
        # Nếu file rỗng hoặc chưa tồn tại, lập tức trả về một danh sách liên kết rỗng
        if not raw_data:
            return data_list
            
        current_line = ""
        
        # Duyệt thủ công từng ký tự để tách dòng 
        for char in raw_data:
            if char == '\n':
                # Khi gặp dấu xuống dòng -> Kết thúc 1 record
                if current_line != "":
                    # Gọi Factory Method của Model để tự nó cắt chuỗi và tạo Object.
                    # Base_repository không cần biết cấu trúc chuỗi có bao nhiêu phần tử.
                    obj = self.model_class.from_file_string(current_line)
                    data_list.append(obj)
                current_line = ""
                
            elif char != '\r': 
                # Bỏ qua ký tự Carriage Return (\r) thường xuất hiện trên hệ điều hành Windows
                current_line += char
                
        # Nếu dòng dữ liệu cuối cùng của file không có dấu xuống dòng (\n)
        if current_line != "":
            obj = self.model_class.from_file_string(current_line)
            data_list.append(obj)
            
        return data_list
    
    def save_data(self, linked_list):
        """
        Duyệt qua LinkedList và ghi đè toàn bộ dữ liệu xuống file.
        Cách làm: Yêu cầu từng Object tự đóng gói dữ liệu của nó thành chuỗi thô 
        rồi lắp ráp tất cả thành một khối chuỗi lớn để ghi đè xuống ổ cứng.
        """
        final_string = ""
        
        # Khởi tạo con trỏ trỏ vào phần tử đầu tiên của LinkedList
        current_node = linked_list.head

        # Duyệt qua từng Node theo cơ chế của danh sách liên kết
        while current_node is not None:
            obj = current_node.value
            
            # Yêu cầu Object tự đóng gói dữ liệu của nó thành chuỗi thô
            final_string += obj.to_file_string() + '\n'
            
            # Di chuyển con trỏ sang Node tiếp theo
            current_node = current_node.next

        # Ghi đè toàn bộ khối chuỗi đã lắp ráp xuống ổ cứng
        self.file_handler.write_file(final_string)
    
    def append_data(self, obj):
        """
        Ghi nối thêm 1 đối tượng mới vào cuối file.
        Dùng cho nghiệp vụ Tạo mới (Create) để tối ưu hiệu năng (O(1) I/O), 
        không cần load toàn bộ file lên và ghi đè lại.
        """
        # Chuyển đối tượng thành chuỗi và kẹp thêm ký tự xuống dòng
        final_string = obj.to_file_string() + '\n'
        
        # Gọi trực tiếp hàm ghi nối của FileHandler
        self.file_handler.append_file(final_string)