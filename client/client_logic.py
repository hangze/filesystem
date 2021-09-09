import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from client_ui import Login_win


class Login_logic:
    login_win = Login_win()

    def get_name(self):
        return self.login_win.user

    def get_pwd(self):
        return self.login_win.pwd

    def get_email(self):
        return self.login_win.email


def on_btn_login_clicked():
    return 1


def change_group():
    return 0
