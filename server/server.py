import base64
import socketserver
from typing import Any

from Crypto.PublicKey import RSA

from basiclib import socket_util
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

from basiclib.common_util import CommonUtil
from server.security_service import SecurityService

security_service=SecurityService()


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
                    ca_book=security_service.get_ca_book()
                    ca_book.update({'response': 'ok'})
                    socket_util.raw_send(self.request, ca_book)
                elif data['type'] == 'send_aes_key':
                    aes_key_encrypt = data['aes_key']

                else:
                    socket_util.send(self.request,{'response': 'fail', 'reason': '认证失败'})
            else:
                if data['type'] == 'get_users':
                    userrrs = []
                    for user in file_server.clients.keys():  # 所有用户列表中遍历
                        if user != self.user:  # 若用户不是我的id，就显示在我的在线列表中传过去
                            userrrs.append(user)
                    socket_util.send(self.request, {'type': 'get_users', 'data': userrrs},
                                     self.aes_key)  # 传回client的'data'为用户[]列表
                # -----------------------------------------------------------------------------------------------------------
                # 获取好友表
                # （传到client方之后 1.直接显示于弹出的框体 2.后面追加"*"表示在线好友 在线好友的获得是使用在线总表与好友表取交集）
                elif data['cmd'] == 'get_friends':
                    fris = []
                    for friend in friend_table[self.user]:  # 在我ID对应的好友list中遍历
                        if friend != self.user:  # 若好友不是我的id，就显示在我的好友表中
                            fris.append(friend)
                    socket_util.send(self.request, {'type': 'get_friends', 'data': fris}, self.aes_key)

    def finish(self):
        if self.authed:
            self.authed = False
            if self.user in file_server.clients.keys():
                del file_server.clients[self.user]
            for user in file_server.clients.keys():
                socket_util.send(file_server.clients[user].request, {'type': 'peer_left', 'peer': self.user},
                                 file_server.clients[user].aes_key)


def handler_init():
    pass


if __name__ == '__main__':
    # 服务端每次运行时，加载用户列表、群组列表
    # todo

    # 接收新客户端的连接请求，递交其IP及端口号至Handler函数，建立线程
    server_port = CommonUtil.get_server_port()
    app = socketserver.ThreadingTCPServer(('0.0.0.0', server_port), file_server)
    app.serve_forever()
