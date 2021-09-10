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
from PIL import Image, ImageTk
from tkinter import ttk

from basiclib.socket_wrapper import SocketConnect










"""
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
        self.win = tk.Toplevel()
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
"""
# -------------------------------------------------------------------------------------
