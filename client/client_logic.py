import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from client_ui import Login_win


class Login_logic:
    ca_public_key = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2CtiLcpfJkOptfZSwB6s
HxZ/Y0vxBpJM25xMnzqAbxotT/ERsRMlEp6u5teSuJkTr4Epc2GGPWodVVpkMWQc
OQFjW3AKgV3SFn8ufvAZ2Q3K8DWyzNH97CPgg/freINiuZmPG32dkucZKtixESqp
dfA4rO9ykFoHbn0QoPZXQTiVuQs3v7uuozOnWifRU7ol5mO9CQu1I4kGy+PiphY6
zjMstmUqxR0JMLRnnRo/p+91mFu46bxupjvoIxVj6lB+1upZZi8PPjfRPUh5BQJj
PUnO+wKP3pXVP+zEVrG3krsG45lLJENVq4i/hrFAuAiQlY5Rpt6wjD9/V7d257ye
9QIDAQAB
-----END PUBLIC KEY-----'''

    login_win = Login_win()

    def get_name(self):
        return self.login_win.user

    def get_pwd(self):
        return self.login_win.pwd

    def get_email(self):
        return self.login_win.email


def on_btn_login_clicked():
    pass


if __name__ == '__main__':
    # str_dir=get_base_disk_dir()
    loginWin = Login_win()
    loginWin.show()
    mainWin = Main_win()
    mainWin.show()
