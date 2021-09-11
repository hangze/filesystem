import os
import queue as Queue
import threading
import tkinter as tk
import tkinter.messagebox
from datetime import time

import time as timer
from socket import socket
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
from tkinter.ttk import Treeview

from PIL import Image, ImageTk

from basiclib import socket_util, crypt_util
from basiclib.common_util import CommonUtil
from basiclib.crypt_util import get_file_md5
from basiclib.file_service import FileService
from basiclib.socket_wrapper import SocketConnect
# from client_ui import Login_win, Main_win
from enity.user import User


class Login_win:
    msg_queue = None  # 创建一个队列

    def handee(self, root):
        # 把队列中的内容取出赋值给label控件
        mpica = self.msg_queue.empty()  # 检查队列是否为空
        if (mpica == False):
            ontad = self.msg_queue.get()
            if (ontad == "file_win"):

                self.destroy()
                client_logic.main_win = Main_Win()
                client_logic.main_win.show()

            elif ontad == "file_win":
                pass

        root.after(500, self.handee, root)  # 递归调用实现循环，TKinter UI线程中无法使用传统的while循环只能用它这个自带的函数递归实现循环

    def show(self):
        self.win.mainloop()  # 接收操作系统发来的事件，然后把事件分发给各个控件和窗体

    def destroy(self):
        self.win.destroy()

    def __init__(self):
        self.msg_queue = Queue.Queue()  # 创建一个队列
        self.win = tk.Tk()  # 窗口
        self.user = tk.StringVar()  # 用户名输入框
        self.email = tk.StringVar()  # 邮箱输入框
        self.pwd = tk.StringVar()  # 密码输入框

        self.win.geometry("320x240")  # 主窗体长*宽
        self.win.title("登录")  # 主窗体标题
        self.win.resizable(width=False, height=False)  # 设置窗口宽不可变，高不可变，默认为True

        # 添加背景图片
        self.img_tk = None
        self.canvas = tk.Canvas(self.win, width=320, height=240)
        img = Image.open('../bg.jpg').resize((320, 240))
        # img = tkinter.PhotoImage(file ='../bg.jpg').resize((320, 240))
        self.img_tk = ImageTk.PhotoImage(img)
        self.canvas.create_image(160, 120, image=self.img_tk)
        self.canvas.pack()

        # 标签 用户名
        self.label1 = tk.Label(self.win, bg="#7FFFAA", font=('宋体', 11))
        self.label1.place(relx=0.12, rely=0.1, height=31, width=50)  # 规定显示框位置以及大小
        self.label1.configure(text='账号')  # 在输入框前显示”账号“两字引导用户输入

        self.entry_user = tk.Entry(self.win)
        self.entry_user.place(relx=0.32, rely=0.11, height=26, relwidth=0.554)  # 规定显示框位置以及大小
        self.entry_user.configure(textvariable=self.user)

        # 标签 邮箱
        self.label1 = tk.Label(self.win, bg="#7D7DFF", font=('宋体', 11))
        self.label1.place(relx=0.12, rely=0.27, height=31, width=50)  # 规定显示框位置以及大小
        self.label1.configure(text='邮箱')  # 在输入框前显示”邮箱“两字引导用户输入

        self.entry_email = tk.Entry(self.win)
        self.entry_email.place(relx=0.32, rely=0.28, height=26, relwidth=0.554)  # 规定显示框位置以及大小
        self.entry_email.configure(textvariable=self.email)

        # 标签 密码
        self.label2 = tk.Label(self.win, bg="#00FFFF", font=('宋体', 11))
        self.label2.place(relx=0.12, rely=0.44, height=31, width=50)  # 规定显示框位置以及大小
        self.label2.configure(text='密码')  # 在输入框前显示”密码“两字引导用户输入

        self.entry_pwd = tk.Entry(self.win)
        self.entry_pwd.place(relx=0.32, rely=0.45, height=26, relwidth=0.554)  # 规定显示框位置以及大小
        self.entry_pwd.configure(show="*")  # 将用户输入的密码显示为”*“以保证密码的安全性
        self.entry_pwd.configure(textvariable=self.pwd)

        # 创建登录按钮
        self.btn_login = tk.Button(self.win, font=('宋体', 11))
        self.btn_login.place(relx=0.13, rely=0.65, height=32, width=88)  # 规定显示框位置以及大小
        self.btn_login.configure(text='登录')  # 显示登录按钮

        # 创建注册按钮
        self.btn_reg = tk.Button(self.win, font=('宋体', 11))
        self.btn_reg.place(relx=0.6, rely=0.65, height=32, width=88)  # 规定显示框位置以及大小
        self.btn_reg.configure(text='注册')  # 显示注册按钮

        # 创建密码按钮
        self.btn_retre_pwd = tk.Button(self.win, font=('宋体', 11))
        self.btn_retre_pwd.place(relx=0.13, rely=0.85, height=32, width=88)  # 规定显示框位置以及大小
        self.btn_retre_pwd.configure(text='密码找回')  # 显示注册按钮

        self.btn_login.configure(command=self.on_btn_login_click)
        self.btn_reg.configure(command=self.on_btn_reg_click)
        self.btn_retre_pwd.configure(command=self.on_btn_retri_pwd_click)

        self.win.after(100, self.handee, self.win)

    def on_btn_login_click(self):
        user_name = self.user.get()
        user_email = self.email.get()
        user_pwd = self.pwd.get()

        client_logic.login(user_name, user_pwd, user_email)

    def on_btn_reg_click(self):
        user_name = self.user.get()
        user_email = self.email.get()
        user_pwd = self.pwd.get()
        client_logic.register(user_name, user_pwd, user_email)

    def on_btn_retri_pwd_click(self):
        user_name = self.user.get()
        user_email = self.email.get()
        user_pwd = self.pwd.get()

        client_logic.retrieve_pwd(user_name, user_email)


# 主窗口 -- 文件列表主界面
class Main_Win:
    closed_fun = None  # 初始化closed_fun
    is_group_space=False
    group_name_cache=""

    def show(self):
        self.win.mainloop()  # 接收操作系统发来的事件，然后把事件分发给各个控件和窗体

    def destroy(self):
        try:
            self.closed_fun()
        except:
            pass
        self.win.destroy()

    def __init__(self):

        self.win = tk.Tk()  # 窗口
        # self.win.focus_force()  # 新窗口获得焦点
        # self.win = tk.Toplevel()
        self.win.protocol('WM_DELETE_WINDOW', self.destroy)  # 关闭之前的窗口
        self.win.geometry("480x320")  # 主窗体长*宽
        self.win.title("磁盘空间")  # 主窗体标题
        self.win.resizable(width=False, height=False)  # 设置窗口宽不可变，高不可变，默认为True

        # self.msg = tk.StringVar()  # 显示输入信息
        # self.name = tk.StringVar()  # 显示用户名
        # self.lsb_option = tk.IntVar() #隐写按钮

        self.win.tree = Treeview(master=self.win, show="tree")  # 定义列的名称
        self.win.tree.place(relx=0.05, rely=0.05, relheight=0.8, relwidth=0.5)

        # 鼠标选中一行回调
        def select_tree(event):
            for item in self.win.tree.selection():
                item_text = self.win.tree.item(item, "values")
                print(item_text)

        self.win.tree.bind(sequence='<ButtonPress-1>', func=select_tree)  # 鼠标双击选中一行

        self.group_list = tk.Listbox(self.win)
        self.group_list.place(relx=0.75, rely=0.15, relheight=0.40, relwidth=0.23)

        # 鼠标双击选中一行回调
        def change_group(event):
            group_name_cache = str(self.group_list.get(self.group_list.curselection()))
            self.group_name_cache =group_name_cache
            self.is_group_space=True
            client_logic.get_group_space(group_name_cache)

        self.group_list.bind(sequence='<Double-Button>', func=change_group)  # 双击切换群组

        self.group_name = tk.StringVar()  # 群组输入框
        self.group_code = tk.StringVar()  # 群组邀请码输入框

        # 标签 群组名称
        self.label_group_name = tk.Label(self.win, bg="#7FFFAA", font=('宋体', 11))
        self.label_group_name.place(relx=0.62, rely=0.55, height=28, width=54)  # 规定显示框位置以及大小
        self.label_group_name.configure(text='群组名')  # 在输入框前显示”群组名称“两字引导用户输入

        self.entry_group_name = tk.Entry(self.win)
        self.entry_group_name.place(relx=0.75, rely=0.56, height=26, relwidth=0.23)  # 规定显示框位置以及大小
        self.entry_group_name.configure(textvariable=self.group_name)

        # 标签 群组邀请码
        self.label_code = tk.Label(self.win, bg="#00FFFF", font=('宋体', 11))
        self.label_code.place(relx=0.62, rely=0.68, height=28, width=54)  # 规定显示框位置以及大小
        self.label_code.configure(text='群组Key')  # 在输入框前显示”群组名称“两字引导用户输入

        self.entry_code = tk.Entry(self.win)
        self.entry_code.place(relx=0.75, rely=0.68, height=26, relwidth=0.23)  # 规定显示框位置以及大小
        self.entry_code.configure(textvariable=self.group_code)

        self.label_group_list = tk.Label(self.win)
        self.label_group_list.place(relx=0.76, rely=0.075, height=21, width=70)  # 规定显示框位置以及大小
        self.label_group_list.configure(text='群组列表')  # 显示该列表为”群组列表“

        self.btn_myspace = tk.Button(self.win)
        self.btn_myspace.place(relx=0.58, rely=0.05, height=28, width=80)
        self.btn_myspace.configure(text='我的空间')

        self.btn_add_group = tk.Button(self.win)
        self.btn_add_group.place(relx=0.75, rely=0.78, height=28, width=110)
        self.btn_add_group.configure(text='添加群组(默认注册)')

        self.btn_upload = tk.Button(self.win)
        self.btn_upload.place(relx=0.5, rely=0.89, height=28, width=108)
        self.btn_upload.configure(text='上传文件')

        self.btn_delete = tk.Button(self.win)
        self.btn_delete.place(relx=0.248, rely=0.89, height=28, width=108)
        self.btn_delete.configure(text='删除文件')

        self.btn_download = tk.Button(self.win)
        self.btn_download.place(relx=0.752, rely=0.89, height=28, width=108)
        self.btn_download.configure(text='下载文件')

        # self.btn_download.configure(state='disabled')

        def on_btn_myspace_click():
            self.is_group_space=False
            self.group_name_cache=""
            client_logic.get_my_space()

        def on_btn_add_group_click():
            group_name = self.group_name.get()
            group_key = self.group_code.get()
            client_logic.add_group(group_name, group_key)

        def on_btn_upload_click():
            print(self.win.tree.item(self.win.tree.focus()))
            file_path = askopenfilename()  # 选择打开什么文件，返回文件名
            file_name = os.path.basename(file_path)
            file_md5 = get_file_md5(file_path)
            client_logic.upload_file(file_path, file_name, file_md5,self.is_group_space,self.group_name_cache)

        def on_btn_download_click():
            file_path = self.win.tree.focus()
            file_name = self.win.tree.item(self.win.tree.focus())["text"]
            file_md5 = ""
            if file_name=="" or file_path=="":
                messagebox.showerror("警告","文件未选择")
            client_logic.download_file(file_path, file_name, file_md5)

        self.btn_myspace.configure(command=on_btn_myspace_click)
        self.btn_add_group.configure(command=on_btn_add_group_click)
        self.btn_upload.configure(command=on_btn_upload_click)
        self.btn_download.configure(command=on_btn_download_click)

        # self.C1 = tk.Checkbutton(self.win, text="开启lsb隐写", variable=self.lsb_option,  onvalue = 1, offvalue = 0)
        # self.C1.place(relx=0.01, rely=0.01, height=57, width=140)

    def show_file_list(self, file_dict: dict):
        self.win.tree.delete(*self.win.tree.get_children())
        i = 0
        if not file_dict:
            return
        for key in file_dict.keys():
            self.win.tree.insert("", 0, file_dict[key], text=key, values=i)
            i = i + 1

    def show_group_list(self, group_list: list):
        self.group_list.delete(0, 'end')
        i = 1
        for group in group_list:
            self.group_list.insert(i, group)
            i = i + 1

    def delButton(self):
        x = self.win.tree.get_children()
        for item in x:
            self.win.tree.delete(item)
    # -------------------------------------------------------------------------------------------------


class Client_Logic:
    login_win = None
    main_win = None
    user = User()

    def __init__(self):
        pass

    def get_name(self):
        return self.login_win.user

    def get_pwd(self):
        return self.login_win.pwd

    def get_email(self):
        return self.login_win.email

    @staticmethod
    def login(user_name, user_pwd, user_email):
        global server_connection
        data_dict = dict()
        data_dict = {"type": "login",
                     "user_name": user_name,
                     "user_pwd": user_pwd,
                     "user_email": user_email
                     }

        server_connection.user.user_name = user_name
        server_connection.user.user_pwd = user_pwd
        server_connection.user.user_email = user_email

        server_connection.send(data_dict)

    @staticmethod
    def register(user_name, user_pwd, user_email):
        global server_connection
        data_dict = dict()
        data_dict = {"type": "register",
                     "user_name": user_name,
                     "user_pwd": user_pwd,
                     "user_email": user_email
                     }
        server_connection.send(data_dict)

    @staticmethod
    def retrieve_pwd(user_name, user_email):
        global server_connection
        data_dict = dict()
        data_dict = {"type": "retrieve_pwd",
                     "user_name": user_name,
                     "user_email": user_email
                     }
        server_connection.send(data_dict)

    @staticmethod
    def retrieve_pwd_verify_code(user_name,new_pwd, verify_code):
        global server_connection
        data_dict = dict()
        data_dict = {"type": "retrieve_pwd_verify_code",
                     "user_name": user_name,
                     "new_pwd":new_pwd,
                     "verify_code": verify_code
                     }
        server_connection.send(data_dict)

    def download_file(self, file_path, file_name, file_md5):
        user_name = server_connection.user.user_name
        token = server_connection.user.user_token
        tmp_aes_key = crypt_util.keyGenerater(16)
        data_dict = dict()
        net_port = 1234
        base_dir = CommonUtil.get_base_disk_dir()
        data_dict = {"type": "download_file",
                     "user_name": user_name,
                     "token": token,
                     "file_path": file_path,
                     "file_name": file_name,
                     "aes_key": tmp_aes_key,
                     "net_port": net_port}
        server_connection.send(data_dict)
        FileService.listen_download_file(net_port, tmp_aes_key, base_dir + "\\" + file_name, file_name, file_md5)

    def upload_file(self, file_local_path, file_name, file_md5,is_group_space=False,group_name=""):
        user_name = server_connection.user.user_name
        token = server_connection.user.user_token
        tmp_aes_key = crypt_util.keyGenerater(16)
        net_ip = server_connection.socket.getpeername()
        data_dict = dict()
        net_port = 1234
        data_dict = {"type": "upload_file",
                     "user_name": user_name,
                     "token": token,
                     "file_path": "",
                     "file_name": file_name,
                     "aes_key": tmp_aes_key,
                     "net_port": net_port,
                     "file_md5": file_md5,
                     "is_group_space":is_group_space,
                     "group_name":group_name}
        server_connection.send(data_dict)

        FileService.upload_file(net_ip[0], net_port, tmp_aes_key, file_local_path)

    def add_group(self, group_name, group_key):
        user_name = server_connection.user.user_name
        token = server_connection.user.user_token
        data_dict = dict()
        data_dict = {"type": "add_group",
                     "user_name": user_name,
                     "token": token,
                     "group_name": group_name,
                     "group_key": group_key}
        server_connection.send(data_dict)

    def get_my_space(self):
        global server_connection
        data_dict = dict()
        data_dict = {"type": "get_my_space",
                     "user_name": server_connection.user.user_name,
                     "token": server_connection.user.user_token
                     }
        server_connection.send(data_dict)

    def get_group_space(self,group_name):
        global server_connection
        data_dict = dict()
        data_dict = {"type": "get_group_space",
                     "user_name": server_connection.user.user_name,
                     "group_name":group_name,
                     "token": server_connection.user.user_token
                     }
        server_connection.send(data_dict)

    def get_my_group(self):
        global server_connection
        data_dict = dict()
        data_dict = {"type": "get_my_group",
                     "user_name": server_connection.user.user_name,
                     "token": server_connection.user.user_token
                     }
        server_connection.send(data_dict)

    def update_info(self):
        timer.sleep(5)
        while True:
            self.get_my_group()
            # self.get_my_space()
            timer.sleep(3)

    def start_update_info(self):
        t2 = threading.Thread(target=self.update_info, args=())  # 为登陆成功的用户创建一个新线程，target为线程执行的函数，
        t2.setDaemon(True)  # 设置：主线程server结束后，子线程（已登录的client用户线程）立即结束
        t2.start()  # 启动该线程

    # 接收服务端消息函数
    # 在用户登陆成功后，为其建立的新线程将调用此函数，接收server发送的数据及相关指令标志
    # 通过标志，在if-else判断逻辑下，实现本机一系列请求后收到应答的处理
    @staticmethod
    def recv_async():
        global server_connection

        while True:
            data = server_connection.recv()  # data为接收到server发送的数据 不同请求（'type'）接收到的消息类型不同
            if data is None:
                continue
            # if data
            if data['type'] == 'operation_msg':
                if data['response'] == 'ok':
                    messagebox.showinfo('成功', data['msg'])

                elif data['response'] == 'fail':
                    messagebox.showerror('警告', data['msg'])
            elif data['type'] == 'login_result':
                if data['response'] == 'ok':
                    server_connection.user.user_token = data['token']
                    messagebox.showinfo('成功', data['msg'])
                    client_logic.login_win.msg_queue.put("file_win")
                    timer.sleep(1)
                    client_logic.start_update_info()
                    print("d")
                elif data['response'] == 'fail':
                    server_connection.user = User()
                    messagebox.showerror('警告', data['msg'])

            elif data['type'] == 'retrieve_pwd_rsp':
                if data['response'] == 'ok':
                    user_name = data['user_name']
                    messagebox.showinfo('成功', data['msg'])
                    # 获取字符串（标题，提示，初始值）
                    newWin = tk.Tk()
                    newWin.withdraw()
                    # retVal = simpledialog.askstring("Enter Value", "Please enter a value", parent=newWin)
                    new_pwd = askstring(parent=newWin,title='获取验证码成功', prompt='请输入新密码', initialvalue='')
                    verify_code = askstring(parent=newWin,title='获取验证码成功', prompt='请输入验证码：', initialvalue='')
                    newWin.destroy()
                    client_logic.retrieve_pwd_verify_code(user_name=user_name,new_pwd=new_pwd, verify_code=verify_code)
                elif data['response'] == 'fail':
                    server_connection.user = User()
                    messagebox.showerror('警告', data['msg'])
            elif data['type'] == 'get_my_space_rsp':
                if data['response'] == 'ok':
                    file_dict = data['file_list']
                    client_logic.main_win.show_file_list(file_dict)

                elif data['response'] == 'fail':
                    server_connection.user = User()
                    messagebox.showerror('警告', data['msg'])
            elif data['type'] == 'get_my_group_rsp':
                if data['response'] == 'ok':
                    group_list = data['group_list']
                    client_logic.main_win.show_group_list(group_list)

                elif data['response'] == 'fail':
                    server_connection.user = User()
                    messagebox.showerror('警告', data['msg'])


server_connection = None
client_logic = None

if __name__ == '__main__':
    # global server_connection
    server_connection = SocketConnect()
    client_logic = Client_Logic()
    client_logic.login_win = Login_win()
    # client_logic.main_win=Main_Win()
    server_connection.connect_to_server(server_ip=CommonUtil.get_server_ip(),
                                        server_port=CommonUtil.get_server_port(), recv_async=client_logic.recv_async)
    client_logic.login_win.show()


def change_group():
    return 0
