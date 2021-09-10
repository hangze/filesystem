import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk

from basiclib.common_util import CommonUtil
from basiclib.socket_wrapper import SocketConnect
from client_ui import Login_win, Main_win

class Login_logic:
    loginWin=None
    # server_connection=None

    # def __init__(self):




    def get_name(self):
        return self.login_win.user

    def get_pwd(self):
        return self.login_win.pwd

    def get_email(self):
        return self.login_win.email


    def login(self,user_name,user_pwd,user_email):
        data_dict=dict()
        data_dict={"type":"login",
                   "user_name":user_name,
                    "user_pwd":user_pwd,
                   "user_email":user_email
                   }
        self.server_connection.send(data_dict)


    # 接收服务端消息函数
    # 在用户登陆成功后，为其建立的新线程将调用此函数，接收server发送的数据及相关指令标志
    # 通过标志，在if-else判断逻辑下，实现本机一系列请求后收到应答的处理
    def recv_async(self):
        global my_socket, users, main_win, current_session, file_transfer_pending, filename_short, filename
        while True:
            data = self.server_connection.recv(my_socket)        # data为接收到server发送的数据 不同请求（'type'）接收到的消息类型不同
            if data['type'] == 'operation_msg':
                if data['response'] == 'ok':
                    tk.messagebox.showinfo('成功',data['msg'])

                elif data['response'] == 'fail':
                    tk.messagebox.showerror('警告', data['msg'])
            if data['type'] == 'get_users':
                users = {}
                users['广场'] = True
                for user in data['data']:   #
                    users[user] = True




if __name__ == '__main__':
    server_connection = SocketConnect()
    server_connection.connect_to_server(server_ip=CommonUtil.get_server_ip(),
                                     server_port=CommonUtil.get_server_port())
    loginWin = Login_win(server_connection)
    loginWin.show()


def change_group():
    return 0

