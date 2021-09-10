class UserDisk:
    file_list = list

    def get_file_list(self):
        return self.file_list

    def add_file(self, file: str):
        self.file_list.append(file)

    def remove_file(self, file: str):
        self.file_list.remove(file)
