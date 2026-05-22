import os

class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        if not os.path.exists(self.file_path):
            return None
        with open(self.file_path, 'r', encoding="utf-8") as file:
            return file.read()

    def write_file(self, data):
        with open(self.file_path, 'w', encoding="utf-8") as file:
            file.write(data)  

    def append_file(self, data):
        with open(self.file_path, 'a', encoding="utf-8") as file:
            file.write(data)