
class Owner():
    pwd_key = ""  # 用户密码的hash形式
    user_name = ""  # 用户名
    user_email = ""  # 用户邮箱
    user_disk_name = ""  # 用户空间名称，实际上是目录名，为随机生成的hash码，与get_base_disk_dir函数返回的路径
    user_file_sec_key = ""  # 用户空间密钥，

    def __init__(self, pwd_key: str, user_name: str, user_email, user_disk_name: str, user_file_sec_key: str):
        self.pwd_key = pwd_key
        self.user_name = user_name
        self.user_email = user_email
        self.user_disk_name = user_disk_name
        self.user_file_sec_key = user_file_sec_key

    def update_pwd(self,new_pwd:str):
        self.pwd_key=new_pwd
