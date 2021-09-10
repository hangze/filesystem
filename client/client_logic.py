import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk

from basiclib.common_util import CommonUtil
from basiclib.socket_wrapper import SocketConnect
# from client_ui import Login_win, Main_win
from enity.user import User




class Login_win:
    def show(self):
        self.win.mainloop()  # 接收操作系统发来的事件，然后把事件分发给各个控件和窗体

    def destroy(self):
        self.win.destroy()

    def __init__(self):

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

        # 创建注册按钮
        self.btn_reg = tk.Button(self.win, font=('宋体', 11))
        self.btn_reg.place(relx=0.13, rely=0.85, height=32, width=88)  # 规定显示框位置以及大小
        self.btn_reg.configure(text='密码找回')  # 显示注册按钮

        self.btn_login.configure(command=self.on_btn_login_click)
        self.btn_reg.configure(command=self.on_btn_reg_click())

    def on_btn_login_click(self):
        user_name = self.user.get()
        user_email = self.email.get()
        user_pwd = self.pwd.get()
        # Login_logic.login(user_name)

    def on_btn_reg_click(self):
        print(self.user.get())
        print(self.email.get())
        print(self.pwd.get())

    def on_btn_reg_click(self):
        global server_connection
        user_name = self.user.get()
        user_email = self.email.get()
        user_pwd = self.pwd.get()
        register_dict={
            "user_name":user_name,
            "user_pwd":user_pwd,
            "user_email":user_email
        }

        # server_connection.send()


# 主窗口 -- 文件列表主界面
class Main_win:
    closed_fun = None  # 初始化closed_fun

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
        # self.win =tk.Toplevel()
        self.win.protocol('WM_DELETE_WINDOW', self.destroy)  # 关闭之前的窗口
        self.win.geometry("480x320")  # 主窗体长*宽
        self.win.title("磁盘空间")  # 主窗体标题
        self.win.resizable(width=False, height=False)  # 设置窗口宽不可变，高不可变，默认为True

        # self.msg = tk.StringVar()  # 显示输入信息
        # self.name = tk.StringVar()  # 显示用户名
        # self.lsb_option = tk.IntVar() #隐写按钮

        self.win.tree = ttk.Treeview(show="tree")  # 定义列的名称
        self.win.tree.place(x=25, y=20, relheight=0.8, relwidth=0.5)

        self.my_id = self.win.tree.insert("", 0, "中国", text="中国China", values="1")  # ""表示父节点是根
        self.my_idx1 = self.win.tree.insert(self.my_id, 0, "广东", text="中国广东", values="2")  # text表示显示出的文本，values是隐藏的值
        self.my_idx2 = self.win.tree.insert(self.my_id, 1, "江苏", text="中国江苏", values="3")
        self.my_idy = self.win.tree.insert("", 1, "美国", text="美国USA", values="4")
        self.my_idy1 = self.win.tree.insert(self.my_idy, 0, "加州", text="美国加州", values="5")

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
            print("got it")
            print(self.group_list.get(self.group_list.curselection()))

        self.group_list.bind(sequence='<Double-Button>', func=change_group)  # 双击切换群组

        self.group_list.insert(1, "fi")
        self.group_list.insert(2, "huang")
        self.group_list.insert(3, "ze")

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
        self.label_code.configure(text='邀请码')  # 在输入框前显示”群组名称“两字引导用户输入

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
        self.btn_add_group.place(relx=0.75, rely=0.78, height=28, width=80)
        self.btn_add_group.configure(text='添加群组')

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
            print('successfully')

        def on_btn_add_group_click():
            print(self.group_name.get())
            print(self.group_code.get())

        def on_btn_upload_click():
            print(self.win.tree.item(self.win.tree.focus()))

        def on_btn_download_click():
            print(self.win.tree.focus())
            print('successfully')

        self.btn_myspace.configure(command=on_btn_myspace_click)
        self.btn_add_group.configure(command=on_btn_add_group_click)
        self.btn_upload.configure(command=on_btn_upload_click)
        self.btn_download.configure(command=on_btn_download_click)

        # self.C1 = tk.Checkbutton(self.win, text="开启lsb隐写", variable=self.lsb_option,  onvalue = 1, offvalue = 0)
        # self.C1.place(relx=0.01, rely=0.01, height=57, width=140)

    # -------------------------------------------------------------------------------------------------




class Client_Logic:
    loginWin=None
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
    def login(user_name,user_pwd,user_email):
        global server_connection
        data_dict=dict()
        data_dict={"type":"login",
                   "user_name":user_name,
                    "user_pwd":user_pwd,
                   "user_email":user_email
                   }
        server_connection.server_connection.send(data_dict)


    # 接收服务端消息函数
    # 在用户登陆成功后，为其建立的新线程将调用此函数，接收server发送的数据及相关指令标志
    # 通过标志，在if-else判断逻辑下，实现本机一系列请求后收到应答的处理
    # @staticmethod
    def recv_async(self):
        global server_connection

        while True:
            data = server_connection.recv()        # data为接收到server发送的数据 不同请求（'type'）接收到的消息类型不同
            if data is None:
                continue
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

server_connection=None

if __name__ == '__main__':
    # global server_connection
    server_connection = SocketConnect()
    client_logic = Client_Logic()
    client_logic.loginWin = Login_win()
    server_connection.connect_to_server(server_ip=CommonUtil.get_server_ip(),
                                     server_port=CommonUtil.get_server_port(),recv_async=client_logic.recv_async)


    client_logic.loginWin.show()


def change_group():
    return 0
