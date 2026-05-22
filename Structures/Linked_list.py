from Structures.Node import Node

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0
        
    def is_empty(self):
        """Kiểm tra danh sách có rỗng hay không"""
        return self.head is None

    def length(self):
        """Trả về số lượng phần tử trong danh sách"""
        return self._size

    def append(self, key):
        """Thêm một phần tử vào CUỐI danh sách"""
        new_node = Node(key)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.right = new_node
            new_node.left = self.tail
            self.tail = new_node
        self._size += 1

    def prepend(self, key):
        """Thêm một phần tử vào ĐẦU danh sách"""
        new_node = Node(key)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.right = self.head
            self.head.left = new_node
            self.head = new_node
        self._size += 1

    def find(self, key):
        """Tìm kiếm giá trị, trả về chỉ số (index) đầu tiên tìm thấy hoặc -1 nếu không có"""
        temp = self.head
        index = 0
        while temp is not None:
            if temp.val == key:
                return index
            temp = temp.right
            index += 1
        return -1

    def remove(self, key):
        """Tìm và xóa phần tử ĐẦU TIÊN có giá trị bằng key. Trả về True nếu xóa thành công."""
        temp = self.head
        while temp is not None:
            if temp.val == key:
                # Trường hợp 1: Node cần xóa là Head
                if temp == self.head:
                    self.head = temp.right
                    if self.head is not None:
                        self.head.left = None
                    else:
                        self.tail = None 
                
                # Trường hợp 2: Node cần xóa là Tail
                elif temp == self.tail:
                    self.tail = temp.left
                    self.tail.right = None
                
                # Trường hợp 3: Node cần xóa nằm ở giữa
                else:
                    temp.left.right = temp.right
                    temp.right.left = temp.left
                
                self._size -= 1
                return True
            
            temp = temp.right 
            
        return False

    def display(self):
        """In danh sách ra màn hình"""
        if self.is_empty():
            print("Danh sách rỗng!")
            return
        
        temp = self.head
        while temp is not None:
            print(temp.val, end=" <-> " if temp.right else "")
            temp = temp.right
        print()