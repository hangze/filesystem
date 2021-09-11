import os
import tkinter
import socket
import io
from datetime import time
import time as timer

from basiclib import socket_util, crypt_util
from basiclib.common_util import CommonUtil
from basiclib.crypt_util import get_file_md5


def file_name_walk(user_disk_dir):
    file_dict=dict()
    for root, dirs, files in os.walk(user_disk_dir):
        print("root", root)  # 当前目录路径
        print("dirs", dirs)  # 当前路径下所有子目录
        print("files", files)  # 当前路径下所有非目录子文件
        if files:
            for file in files:
                file_dict[file]=root+"\\"+file
    return file_dict


class FileService:

    # 创建用户的磁盘空间,并返回绝对路径
    @staticmethod
    def create_user_disk( user_name: str):
        base_dir = CommonUtil.get_base_disk_dir()
        user_disk_dir = base_dir + "\\" + user_name
        if not os.path.exists(user_disk_dir):
            os.mkdir(user_disk_dir)
        return user_disk_dir


    @staticmethod
    def save_file_encrypt(file_path,file_data ,aes_key):
        f= open(file_path, 'rb')
        encrypt_data = crypt_util.encrypt_byte(aes_key, file_data)
        f.write(encrypt_data)

    @staticmethod
    def load_file_encrypt(file_path, aes_key):
        file_data=None
        with open(file_path, 'rb') as f:
            file_data = f.read()
        decrypt_file_data = crypt_util.decrypt_byte(aes_key, file_data)
        return decrypt_file_data

    @staticmethod
    def get_user_disk_dir(user_name: str):
        base_dir = CommonUtil.get_base_disk_dir()
        user_disk_dir = base_dir + "\\" + user_name
        if not os.path.exists(user_disk_dir):
            os.mkdir(user_disk_dir)
        return user_disk_dir


    @staticmethod
    def ger_user_file_list(user_name):
        base_dir = CommonUtil.get_base_disk_dir()
        user_disk_dir = base_dir + "\\" + user_name
        return file_name_walk(user_disk_dir)

    @staticmethod
    def upload_file(net_ip,net_port,aes_key,file_path,is_show_msg=True):
        total_bytes = 0
        starttime = timer.time()
        addr = (net_ip, net_port)
        tmp_aes_key = aes_key
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(addr)
        except:
            timer.sleep(5)
            client.connect(addr)
        with open(file_path, 'rb') as f:
            file_data = f.read()
            encrypt_data = crypt_util.encrypt_byte(tmp_aes_key, file_data)
            bytes_stream = io.BytesIO(encrypt_data)
            while True:
                fdata = bytes_stream.read(1024)
                if not fdata:
                    break
                total_bytes += len(fdata)
                client.send(fdata)
        f.close()
        client.close()
        endtime = timer.time()
        if is_show_msg:
            tkinter.messagebox.showinfo('注意', '文件传送成功！,Transform %s bytes from %s in %s seconds\n' % (
                total_bytes, "server", format(0 - 0, '.2f')))

    @staticmethod
    def listen_download_file(net_port, aes_key, file_save_path,file_name,file_md5,is_show_msg=True):
        total_bytes = 0
        addr = ('0.0.0.0', net_port)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(addr)
        server.listen(5)
        client_socket, addr = server.accept()
        # starttime = time.time()
        bytes_stream = io.BytesIO()
        f = open(file_save_path, "wb")
        while True:
            fdata = client_socket.recv(1024)
            total_bytes += len(fdata)
            if not fdata:
                break
            bytes_stream.write(fdata)
        bytes_stream.seek(0)
        file_data = crypt_util.decrypt_byte(aes_key, bytes_stream.read())
        f.write(file_data)
        f.close()
        client_socket.close()
        server.close()
        # endtime = time.time()
        received_file_md5 = get_file_md5(file_save_path)
        if received_file_md5 == file_md5:
            if is_show_msg:
                tkinter.messagebox.showinfo('注意', '文件比对成功！,Received %s bytes from %s in %s seconds\n' % (
                    total_bytes, "server", format(0 - 0, '.2f')))
        if is_show_msg:
            tkinter.messagebox.showinfo('注意', '文件比对成功！,Received %s bytes from %s in %s seconds\n' % (
                total_bytes, "server", format(0 - 0, '.2f')))





