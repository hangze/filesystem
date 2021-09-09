import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from client_ui import Login_win, Main_win

ca_public_key = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2CtiLcpfJkOptfZSwB6s
HxZ/Y0vxBpJM25xMnzqAbxotT/ERsRMlEp6u5teSuJkTr4Epc2GGPWodVVpkMWQc
OQFjW3AKgV3SFn8ufvAZ2Q3K8DWyzNH97CPgg/freINiuZmPG32dkucZKtixESqp
dfA4rO9ykFoHbn0QoPZXQTiVuQs3v7uuozOnWifRU7ol5mO9CQu1I4kGy+PiphY6
zjMstmUqxR0JMLRnnRo/p+91mFu46bxupjvoIxVj6lB+1upZZi8PPjfRPUh5BQJj
PUnO+wKP3pXVP+zEVrG3krsG45lLJENVq4i/hrFAuAiQlY5Rpt6wjD9/V7d257ye
9QIDAQAB
-----END PUBLIC KEY-----'''

class Login_logic:
    login_win = Login_win()

    def get_name(self):
        return self.login_win.user

    def get_pwd(self):
        return self.login_win.pwd

    def get_email(self):
        return self.login_win.email


def on_btn_login_clicked():
    pass


# 接收服务端消息函数
# 在用户登陆成功后，为其建立的新线程将调用此函数，接收server发送的数据及相关指令标志
# 通过标志，在if-else判断逻辑下，实现本机一系列请求后收到应答的处理
def recv_async():
    global my_socket, users, main_win, current_session, file_transfer_pending, filename_short, filename, friends
    while True:
        data = server_connection.recv(my_socket)        # data为接收到server发送的数据 不同请求（'type'）接收到的消息类型不同
        if data['type'] == 'operation_msg':
            if data['response'] == 'ok':
                tkinter.messagebox.showinfo('成功',data['msg'])

            elif data['response'] == 'fail':
                tkinter.messagebox.showerror('警告', data['msg'])

        if data['type'] == 'get_users':
            users = {}
            users['广场'] = True
            for user in data['data']:   #
                users[user] = True
            refresh_user_list()

    # -------------------------------------------------------------------------------------------
        elif data['type'] == 'get_friends':
            friends = {}
            for fri in data['data']:
                friends[fri] = True
            refresh_friend_list(friends)



if __name__ == '__main__':
    # str_dir=get_base_disk_dir()
    loginWin = Login_win()
    loginWin.show()
    mainWin = Main_win()
    mainWin.show()


def change_group():
    return 0

