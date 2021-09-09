# -*- coding: utf-8 -*
import os

# 获取网络磁盘基本目录，基本目录下是各个用户的目录
# @return 返回基本目录，如 C:\\User\\document:
class CommonUtil():

    @staticmethod
    def get_base_disk_dir():
        curr_dir=os.getcwd()
        return curr_dir

    @staticmethod
    def get_server_ip():
        server_ip="127.0.0.1"
        return server_ip

    @staticmethod
    def get_server_port():
        server_port=8888
        return server_port


def get_base_disk_dir():
    return None