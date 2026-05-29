from Structures.Node import Node

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def is_empty(self):
        return self.head is None

    def length(self):
        return self._size
    
    def append(self, key, value):
        new_node = Node(key, value)

        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self._size += 1

    def prepend(self, key, value):
        new_node = Node(key, value)
        
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def find(self, key):
        temp = self.head
        index = 0
        while temp is not None:
            if temp.key == key:
                return index
            temp = temp.next
            index += 1
        return -1

    def remove(self, key):
        temp = self.head
        while temp is not None:
            if temp.key == key:
                if temp == self.head:
                    self.head = temp.next
                    if self.head is not None:
                        self.head.prev = None
                    else:
                        self.tail = None
                elif temp == self.tail:
                    self.tail = temp.prev
                    self.tail.next = None
                else:
                    temp.prev.next = temp.next
                    temp.next.prev = temp.prev
                self._size -= 1
                return True
            temp = temp.next
        return False

    def display(self):
        if self.is_empty():
            print("Danh sách rỗng!")
            return
        temp = self.head
        while temp is not None:
            print(f"({temp.key}: {temp.value})", end=" <-> " if temp.next else "")
            temp = temp.next
        print()