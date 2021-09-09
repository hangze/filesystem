#
import base64
import time
import tkinter

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import struct
import json
import socket
import utils
from socket_util import *

class SocketConnect:

    server_public_key=""
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.settimeout(10)
        self.max_buff_size = 1024  # 单次最大传输数据大小
        self.aes_key = b''  #会话密钥，本地生成


    def connect_to_server(self, server_ip, server_port,server_public_key):
        self.server_public_key = server_public_key
        self.socket.connect((server_ip, int(server_port)))
        #客户端生成私钥
        aes_key = utils.keyGenerater(16)
        self.aes_key = aes_key.encode()
        cipher = PKCS1_cipher.new(self.server_public_key)
        encrypt_aes_key = base64.b64encode(cipher.encrypt(bytes(aes_key.encode("utf8"))))

        #生成时间戳
        time_stamp=str(time.time_ns())
        # 用公钥生成签名

        self.raw_send(self.socket, {'cmd': 'send_private_key', 'aes_key': encrypt_aes_key,'time_stamp':time_stamp,'signture':})
        server_response = self.recv(self.socket)
        if server_response['response'] == 'ok':
            # 获取aes密钥成功，
            raw_aes_key = server_response['aes_key']
            decrypt_rsa_key = self.private_cipher.decrypt(base64.b64decode(raw_aes_key), 0)
            self.aes_key = decrypt_rsa_key  # .decode('utf-8')

        else:
            tkinter.messagebox.showerror('警告', '传送私钥,请查看网络连接后重新启动' + server_response['reason'])
            utils.close_socket()

    def p2p_connect(self, server_ip, server_port,private_key):
        self.socket.connect((server_ip, int(server_port)))
        self.raw_send(self.socket, {'cmd': 'get_private_key', 'public_key': self.public_key})
        server_response = self.recv(self.socket)
        if server_response['response'] == 'ok':
            # 获取aes密钥成功，
            raw_aes_key = server_response['aes_key']
            decrypt_rsa_key = self.private_cipher.decrypt(base64.b64decode(raw_aes_key), 0)
            self.aes_key = decrypt_rsa_key  # .decode('utf-8')

        else:
            tkinter.messagebox.showerror('警告', '传送私钥失败,请查看网络连接后重新启动' + server_response['reason'])
            utils.close_socket()

    def close_socket(self):
        self.send(self.socket, {'cmd': 'close'})
        self.socket.shutdown(2)
        self.socket.close()

    # 使用socket收-发数据
    def send(self, data_dict):
        send(self.socket,data_dict,1)

    # 使用socket收-发数据,不加密
    def raw_send(self, data_dict):
        raw_send(self.socket,data_dict)

    def recv(self):
        return recv(self.socket,self.aes_key)

    def raw_recv(self):
        return raw_recv(self.socket)

