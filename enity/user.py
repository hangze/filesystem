# 用户对象，持有用户相关属性，以及若干函数
from enity.owner import Owner


class User(Owner):
    user_group = list()
    user_token=None

    def __init__(pwd_key: str, user_name: str, user_email, user_disk_name: str, user_file_sec_key: str):
        super().__init__(pwd_key,user_name, user_email, user_disk_name, user_file_sec_key)

    def __init__(self):
        pass

    def add_group(self, group_name):
        if group_name not in self.user_group:
            self.user_group.append(group_name)

