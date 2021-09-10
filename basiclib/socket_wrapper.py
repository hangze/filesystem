#
import base64
import socket
import tkinter

import utils
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.PublicKey import RSA

from basiclib.common_util import CommonUtil
from basiclib.crypt_util import verify_signture, keyGenerater
# import * from socket_util
from basiclib.socket_util import raw_send, recv, raw_recv, send


class SocketConnect:
    server_public_key = ""

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.settimeout(10)
        self.max_buff_size = 1024  # 单次最大传输数据大小
        self.aes_key = b''  # 会话密钥，本地生成

    def connect_to_server(self, server_ip, server_port):
        try:
            self.socket.connect((server_ip, int(server_port)))
            # 客户端生成私钥
            # aes_key = keyGenerater(16)
            # self.aes_key = aes_key.encode()
            # cipher = PKCS1_cipher.new(self.server_public_key)
            # encrypt_aes_key = base64.b64encode(cipher.encrypt(bytes(aes_key.encode("utf8"))))

            self.raw_send({'type': 'get_ca_book'})
            server_response = self.recv()
            if server_response['response'] == 'ok':
                # 获取ca证书成功，验证签名
                data_dict = dict()
                data_dict["server_ip"] = server_ip
                data_dict["server_port"] = server_port
                data_dict["server_pub_key"] = server_response["server_pub_key"]
                self.server_public_key = server_response["server_pub_key"]
                str_signture = server_response['signture']
                if verify_signture(data_dict, bytes(str_signture,encoding = "utf8"), CommonUtil.get_ca_private_key()):
                    # 认证成功，发送密钥
                    # 客户端生成私钥
                    aes_key = keyGenerater(16)
                    self.aes_key = aes_key.encode()
                    pub_key = RSA.importKey(self.server_public_key)
                    cipher = PKCS1_cipher.new(pub_key)
                    aes_key_encrypt = base64.b64encode(cipher.encrypt(bytes(aes_key.encode("utf8"))))
                    self.raw_send({'type': 'send_aes_key', 'aes_key_encrypt': aes_key_encrypt.decode()})
                    aes_response = self.recv()
                    if aes_response['response'] == 'ok':
                        print("与服务端交换密钥完成")
                    else:
                        print("与服务端交换密钥失败")
                        raise Exception("与服务端交换密钥失败")
                else:
                    # 验签失败
                    tkinter.messagebox.showerror('警告', '验签失败，服务端不可信' + server_response['reason'])
                    self.close_socket()
            else:
                tkinter.messagebox.showerror('警告', '传送私钥失败,请查看网络连接后重新启动' + server_response['reason'])
                self.close_socket()
        except Exception as e:
            print(e.__str__())
            # tkinter.messagebox.showerror('警告', e.__str__())
            raise e
            self.close_socket()

    def p2p_connect(self, server_ip, server_port, private_key):
        self.socket.connect((server_ip, int(server_port)))
        self.raw_send({'cmd': 'get_private_key', 'public_key': self.public_key})
        server_response = self.recv()
        if server_response['response'] == 'ok':
            # 获取aes密钥成功，
            raw_aes_key = server_response['aes_key']
            decrypt_rsa_key = self.private_cipher.decrypt(base64.b64decode(raw_aes_key), 0)
            self.aes_key = decrypt_rsa_key  # .decode('utf-8')

        else:
            tkinter.messagebox.showerror('警告', '传送私钥失败,请查看网络连接后重新启动' + server_response['reason'])
            utils.close_socket()

    def close_socket(self):
        self.send({'cmd': 'close'})
        self.socket.shutdown(2)
        self.socket.close()

    # 使用socket收-发数据
    def send(self, data_dict):
        try:
            send(self.socket, data_dict, 1)
        except Exception as e:
            print(e)

    # 使用socket收-发数据,不加密
    def raw_send(self, data_dict):
        try:
            raw_send(self.socket, data_dict)
        except Exception as e:
            print(e)

    def recv(self):
        try:
            return recv(self.socket, self.aes_key)
        except Exception as e:
            print(e)

    def raw_recv(self):
        try:
            return raw_recv(self.socket)
        except Exception as e:
            print(e)
