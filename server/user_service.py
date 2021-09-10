import os
import pickle
import time
from hashlib import sha1

from basiclib.common_util import CommonUtil
from basiclib.mail_util import MailServer
from enity.user import User
from file_service import FileService


class UserService:
    # 保持已登录的token，现实中一般还会做刷新和过期操作
    token_dict = dict()
    user_dict = dict()
    user_name_verify_code = dict()

    def __init__(self):
        self.load_token_dict()
        self.load_user_dict()

    # @staticmethod

    def save_user_dict(self):
        CommonUtil.save_data("user_dict.dat", self.user_dict)

    def load_user_dict(self):
        user_dict = CommonUtil.load_data("user_dict.dat")
        if user_dict:
            self.user_dict=user_dict

    def save_token_dict(self):
       CommonUtil.save_data("token_dict.dat", self.token_dict)

    def load_token_dict(self):
        token_dict= CommonUtil.load_data("token_dict.dat")
        if token_dict:
            self.token_dict =token_dict

    # 登录后添加token
    def add_token(self, token: str):
        if token not in self.token_dict:
            self.token_dict.add(token)

    # 判断token是否仍处于有效状态
    def is_login(self, token: str):
        if token in self.token_dict:
            return True
        return False

    def login(self, user_name, user_pwd):
        if user_name not in self.user_dict.keys():
            raise Exception("用户不存在")
        if user_pwd == self.user_dict[user_name].pwd_key:
            print("密码正确，登录成功")
            token = sha1(os.urandom(24)).hexdigest()
            self.token_dict[token] = user_name
            self.save_token_dict()
            return token

    def register(self, user_name, user_pwd, user_email):
        if user_name in self.user_dict.keys():
            raise Exception("用户已存在，请更改用户名")

        user = User()
        user.user_name=user_name
        user.user_email=user_email
        user.pwd_key=user_pwd
        # 创建用户文件目录
        # 创建用户file_key，用于加密文件
        user_dir = FileService.create_user_disk(user_name=user_name)
        user.user_disk_name = user_dir
        user.user_file_sec_key = sha1(os.urandom(24)).hexdigest()
        self.user_dict.update({user_name: user})
        self.save_user_dict()

    def retrive_pwd(self, user_name, user_email):
        verify_code = str(time.time() % 1000000)
        main_server = MailServer()
        main_server.send_verify_mail(verify_code=verify_code, des_mail_addr=user_email)
        self.user_name_verify_code.update({user_name: verify_code})

    def retrive_pwd_verify(self, user_name: str, user_email: str, user_new_pwd, user_verify_code: str):
        if user_name in self.user_name_verify_code.keys():
            if user_verify_code == self.user_name_verify_code[user_name]:
                self.user_dict[user_name].update_pwd(user_new_pwd)
                self.save_user_dict()
                return True
        raise Exception("验证失败")
