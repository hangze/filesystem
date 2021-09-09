import base64
import io
import socketserver
import tkinter.filedialog
import tkinter.messagebox
import tkinter as tk
import threading
import hashlib
import socket
import time
import sys
import os

from typing import Any

from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.PublicKey import RSA

import utils
from PIL import Image, ImageTk
from communication import ClientConnect as Connection


class Login_win:

    def show(self):
        self.win.mainloop()  # 接收操作系统发来的事件，然后把事件分发给各个控件和窗体

    def destroy(self):
        self.win.destroy()

    def __init__(self):
        self.win = tk.Tk()  # 窗口
        self.user = tk.StringVar()  # 用户名输入框
        self.pwd = tk.StringVar()  # 密码输入框

        self.win.geometry("320x240")  # 主窗体长*宽
        self.win.title("登录")  # 主窗体标题
        self.win.resizable(width=False, height=False)  # 设置窗口宽不可变，高不可变，默认为True

        # 添加背景图片
        self.img_tk = None
        self.canvas = tk.Canvas(self.win, width=320, height=240)
        img = Image.open('./bg.jpg').resize((320, 240))
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

        # 标签 密码
        self.label2 = tk.Label(self.win, bg="#00FFFF", font=('宋体', 11))
        self.label2.place(relx=0.12, rely=0.27, height=31, width=50)  # 规定显示框位置以及大小
        self.label2.configure(text='密码')  # 在输入框前显示”密码“两字引导用户输入

        self.entry_pwd = tk.Entry(self.win)
        self.entry_pwd.place(relx=0.32, rely=0.28, height=26, relwidth=0.554)  # 规定显示框位置以及大小
        self.entry_pwd.configure(show="*")  # 将用户输入的密码显示为”*“以保证密码的安全性
        self.entry_pwd.configure(textvariable=self.pwd)

        # 创建登录按钮
        self.btn_login = tk.Button(self.win, font=('宋体', 11))
        self.btn_login.place(relx=0.13, rely=0.6, height=32, width=88)  # 规定显示框位置以及大小
        self.btn_login.configure(text='登录')  # 显示登录按钮
        # 创建注册按钮
        self.btn_reg = tk.Button(self.win, font=('宋体', 11))
        self.btn_reg.place(relx=0.6, rely=0.6, height=32, width=88)  # 规定显示框位置以及大小
        self.btn_reg.configure(text='注册')  # 显示注册按钮


# 主窗口 -- 聊天界面
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
        #self.win =tk.Toplevel()
        self.win.protocol('WM_DELETE_WINDOW', self.destroy)  # 关闭之前的窗口
        self.win.geometry("480x320")  # 主窗体长*宽
        self.win.title("聊天室")  # 主窗体标题
        self.win.resizable(width=False, height=False)  # 设置窗口宽不可变，高不可变，默认为True

        self.msg = tk.StringVar()  # 显示输入信息
        self.name = tk.StringVar()  # 显示用户名
        self.lsb_option = tk.IntVar() #隐写按钮

        self.user_list = tk.Listbox(self.win)
        self.user_list.place(relx=0.75, rely=0.15, relheight=0.72, relwidth=0.23)  # 规定显示框位置以及大小

        self.label1 = tk.Label(self.win)
        self.label1.place(relx=0.76, rely=0.075, height=21, width=101)  # 规定显示框位置以及大小
        self.label1.configure(text='在线用户列表')  # 显示该列表为”在线用户列表“

        self.history = tk.Text(self.win)
        self.history.place(relx=0.02, rely=0.24, relheight=0.63, relwidth=0.696)
        self.history.configure(state='disabled')

        self.entry_msg = tk.Entry(self.win)
        self.entry_msg.place(relx=0.02, rely=0.9, height=24, relwidth=0.59)
        self.entry_msg.configure(textvariable=self.msg)

        self.btn_send = tk.Button(self.win)
        self.btn_send.place(relx=0.62, rely=0.89, height=28, width=45)
        self.btn_send.configure(text='发送')

        self.btn_file = tk.Button(self.win)
        self.btn_file.place(relx=0.752, rely=0.89, height=28, width=108)
        self.btn_file.configure(text='发送文件')
        self.btn_file.configure(state='disabled')

        self.label2 = tk.Label(self.win)
        self.label2.place(relx=0.24, rely=0.0, height=57, width=140)
        self.label2.configure(textvariable=self.name)

        self.C1 = tk.Checkbutton(self.win, text="开启lsb隐写", variable=self.lsb_option,  onvalue = 1, offvalue = 0)
        self.C1.place(relx=0.01, rely=0.01, height=57, width=140)

    # -------------------------------------------------------------------------------------------------
class Friends_win:
    closed_fun = None

    def show(self):
        self.win.mainloop()

    def destroy(self):
        try:
            self.closed_fun()
        except:
            pass
        self.win.destroy()

    def __init__(self):
        # self.win = tk.Tk()  # 窗口
        self.win =tk.Toplevel()
        self.add = tk.StringVar()  # 添加好友输入框
        self.delete = tk.StringVar()  # 删除好友操作输入框

        self.win.geometry("560x320")  # 主窗体长*宽
        self.win.title("好友列表")  # 好友表窗体标题
        self.win.resizable(width=False, height=False)

        # 两个button
        self.btn_add = tk.Button(self.win)
        self.btn_add.place(relx=0.055, rely=0.1, height=31, width=89)
        self.btn_add.configure(text='添加好友')

        self.btn_delete = tk.Button(self.win)
        self.btn_delete.place(relx=0.055, rely=0.27, height=31, width=89)
        self.btn_delete.configure(text='删除好友')

        # 两个entry：add delete
        self.entry_add = tk.Entry(self.win)
        self.entry_add.place(relx=0.28, rely=0.11, height=26, relwidth=0.3)  # 规定显示框位置以及大小
        self.entry_add.configure(textvariable=self.add)

        self.entry_delete = tk.Entry(self.win)
        self.entry_delete.place(relx=0.28, rely=0.28, height=26, relwidth=0.3)  # 规定显示框位置以及大小
        self.entry_delete.configure(textvariable=self.delete)

        # 显示好友列表
        self.label = tk.Label(self.win)
        self.label.place(relx=0.76, rely=0.075, height=21, width=101)  # 规定显示框位置以及大小
        self.label.configure(text='在线好友列表')

        self.friends_list = tk.Listbox(self.win)  # 好友列表
        self.friends_list.place(relx=0.75, rely=0.15, relheight=0.72, relwidth=0.23)  # 规定显示框位置以及大小

# -------------------------------------------------------------------------------------