import base64
import socketserver
from typing import Any

from Crypto.PublicKey import RSA

from basiclib import socket_util
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

from basiclib.common_util import CommonUtil
from security_service import SecurityService
from user_service import UserService

security_service = SecurityService()
user_service = UserService()
hanler_dict = dict()


class file_server(socketserver.BaseRequestHandler):
    # 当有client请求连接时，对应创建一个BaseRequestHandler类
    # 并为其创建一个新线程，实现接收消息、完成对应功能
    clients = {}

    def __init__(self, request: Any, client_address: Any, server: socketserver.BaseServer):
        super().__init__(request, client_address, server)
        self.aes_key = ''

    def setup(self):
        self.user = ''
        self.file_peer = ''
        self.aes_key = ''
        self.self_public_key = ''
        self.authed = False

    def handle(self):
        while True:
            data = socket_util.recv(self.request, self.aes_key)  # data 为接收到的client所发送的数据字典
            if not self.authed:
                if data['type'] == 'get_ca_book':
                    ca_book = security_service.get_ca_book()
                    ca_book.update({'response': 'ok'})
                    socket_util.raw_send(self.request, ca_book)
                elif data['type'] == 'send_aes_key':
                    aes_key_encrypt = data['aes_key_encrypt']
                    aes_key_decrypt = security_service.decrypt_data(aes_key_encrypt)
                    self.aes_key = aes_key_decrypt
                    socket_util.raw_send(self.request, {'response': 'ok', 'reason': '认证成功'})
                    self.authed = True
                else:
                    socket_util.raw_send(self.request, {'response': 'fail', 'reason': '认证失败'})
            else:

                if data["type"] == "retrieve_pwd":
                    user_name = data["user_name"]
                    user_email = data["user_email"]
                    try:
                        user_service.retrive_pwd(user_name=user_name,user_email=user_email)
                        socket_util.send(self.request, {'response': 'ok', 'msg': '验证码发送成功'}, self.aes_key)
                    except Exception as e:
                        socket_util.send(self.request, {'response': 'fail', 'msg': str(e.message)}, self.aes_key)

                elif data["type"] == "retrieve_pwd_code":
                    user_name = data["user_name"]
                    user_email = data["user_email"]
                    user_new_pwd=data["user_new_pwd"]
                    user_verify_code=data["user_verify_code"]
                    try:
                        user_service.retrive_pwd_verify(user_name=user_name, user_email=user_email,user_verify_code=user_verify_code)
                        socket_util.send(self.request, {'response': 'ok', 'msg': '密码重置成功'}, self.aes_key)
                    except Exception as e:
                        socket_util.send(self.request, {'response': 'fail', 'msg': str(e.message)}, self.aes_key)


                elif data["type"] == "register":
                    user_name = data["user_name"]
                    user_pwd = data["user_pwd"]
                    user_email=data["user_email"]
                    try:
                        user_service.register(user_name=user_name, user_pwd=user_pwd, user_email=user_email)
                        socket_util.send(self.request, {'response': 'ok','msg': '注册成功'}, self.aes_key)
                    except Exception as e:
                        socket_util.send(self.request, {'response': 'fail', 'msg': '注册失败'}, self.aes_key)
                elif data["type"] == "login":
                    user_name = data["user_name"]
                    user_pwd = data["user_pwd"]
                    try:
                        token = user_service.login(user_name, user_pwd)
                        socket_util.send(self.request, {'response': 'ok', 'token': token, 'msg': '认证成功'}, self.aes_key)
                    except Exception as e:
                        socket_util.send(self.request, {'response': 'fail', 'msg': '认证失败'}, self.aes_key)
                        # -----------------------------------------------------------------------------------------------------------
                elif data['token'] == '':
                    socket_util.send(self.request, {'type': 'operation_msg', 'msg': "请登录"}, self.aes_key)
                else:
                    # 验证token是否有效
                    if user_service.is_login(token):
                        pass
                        # if data["type"] ="":
                        #     hanler_dict[data["type"]](data)
                        # elif data["type"] ="":
                        #     pass
                        # elif data["type"] ="":
                        #     pass
                        # elif data["type"] ="":
                        #     pass
                        # elif data["type"] ="":
                        #     pass
                        # elif data["type"] ="":
                        #     pass
                        # elif data["type"] ="":
                        #     pass
                    else:
                        socket_util.send(self.request, {'type': 'operation_msg', 'msg': "token无效，请重新登录"}, self.aes_key)

    def finish(self):
        if self.authed:
            self.authed = False
            if self.user in file_server.clients.keys():
                del file_server.clients[self.user]
            for user in file_server.clients.keys():
                socket_util.send(file_server.clients[user].request, {'type': 'peer_left', 'peer': self.user},
                                 file_server.clients[user].aes_key)


def handler_init():
    global hanler_dict
    # hanler_dict["get_file_list"] =


if __name__ == '__main__':
    # 服务端每次运行时，加载用户列表、群组列表
    # todo

    # 接收新客户端的连接请求，递交其IP及端口号至Handler函数，建立线程
    server_port = CommonUtil.get_server_port()
    app = socketserver.ThreadingTCPServer(('0.0.0.0', server_port), file_server)
    app.serve_forever()
