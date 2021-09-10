from enity.owner import Owner


# 群组，继承自User
class Group(Owner):
    group_member=[]

    def __init__(self, pwd_key: str, user_name: str, user_disk_name: str, user_file_sec_key: str):
        super().__init__(pwd_key,user_name,user_disk_name,user_file_sec_key)

    def add_group_member(self,user_name):
        if user_name not in self.group_member:
            self.group_member.append(user_name)

    def remove_group_member(self,user_name):
        if user_name in self.group_member:
            self.group_member.remove(user_name)