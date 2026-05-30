from Structures.Node import Node
from Structures.Linked_list import LinkedList
class Hash_table:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.table = [None] * self.capacity 
        self.size = 0

    #  HÀM BĂM 
    def custom_hash(self, key):
        hash_val = 0
        
        if type(key) == str:
            for char in key:
                hash_val = (hash_val * 31 + ord(char)) % self.capacity
        elif type(key) == int:
            hash_val = key % self.capacity
        return hash_val

    def insert(self, key, value):
        index = self.custom_hash(key)
        

        if self.table[index] is None:
            self.table[index] = Node(key, value)
            self.size += 1
            return
        

        current = self.table[index]
        while current is not None:

            if current.key == key:
                current.value = value
                return
            

            if current.next is None:
                break
            current = current.next
            

        current.next = Node(key, value)
        self.size += 1

    def search(self, key):
        index = self.custom_hash(key)
        current = self.table[index]
        

        while current is not None:
            if current.key == key:
                return current.value 
            current = current.next
            
        return None  

    def remove(self, key):
        index = self.custom_hash(key)
        current = self.table[index]
        prev = None
        
        while current is not None:
            if current.key == key:

                if prev is None:
                    self.table[index] = current.next

                else:
                    prev.next = current.next
                
                self.size -= 1
                return True 
            
            prev = current
            current = current.next
            
        return False

    def display(self):
        print(f"{'-'*45}\nTrạng thái Hash Table (Từ con số 0):\n{'-'*45}")

        for i in range(self.capacity):
            current = self.table[i]
            if current is None:
                print(f"Bucket {i:02}: [ Trống ]")
            else:
                items = ""
                while current is not None:
                    items += f"({current.key}: {current.value}) -> "
                    current = current.next
                items += "None"
                print(f"Bucket {i:02}: {items}")

    def values(self):

        result = LinkedList()

        for bucket in self.table:

            current = bucket

            while current is not None:

                result.append(
                    current.key,
                    current.value
                )

                current = current.next

        return result