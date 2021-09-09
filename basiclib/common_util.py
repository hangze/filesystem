# -*- coding: utf-8 -*
import os

# 获取网络磁盘基本目录，基本目录下是各个用户的目录
# @return 返回基本目录，如 C:\\User\\document:
def get_base_disk_dir():
    curr_dir=os.getcwd()
    return curr_dir
