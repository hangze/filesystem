import base64
import socketserver
from typing import Any

from Crypto.PublicKey import RSA

from basiclib import socket_wrapper
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher


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
            data = socket_wrapper.recv(self.request, self.aes_key)  # data 为接收到的client所发送的数据字典
            if not self.authed:
                if data['cmd'] == 'get_private_key':
                    public_key = data['public_key']
                    pub_key = RSA.importKey(public_key)
                    self.self_public_key = public_key
                    cipher = PKCS1_cipher.new(pub_key)
                    aes_key = socket_wrapper.keyGenerater(16)
                    self.aes_key = aes_key.encode()
                    encrypt_aes_key = base64.b64encode(cipher.encrypt(bytes(aes_key.encode("utf8"))))
                    socket_wrapper.raw_send(self.request, {'response': 'ok', 'aes_key': encrypt_aes_key.decode()})
                else:
                    self.user = data['user']
                    if data['cmd'] == 'login':  # 本地实现登录请求
                        if validate(data['user'], data['pwd']):
                            socket_wrapper.send(self.request, {'response': 'ok'}, self.aes_key)
                            self.authed = True
                            for user in file_server.clients.keys():
                                socket_wrapper.send(file_server.clients[user].request,
                                                    {'type': 'peer_joined', 'peer': self.user},
                                                    file_server.clients[user].aes_key)
                            file_server.clients[self.user] = self
                        else:
                            socket_wrapper.send(self.request, {'response': 'fail', 'reason': '账号或密码错误！'}, self.aes_key)
                    elif data['cmd'] == 'register':
                        if register(data['user'], data['pwd']):
                            socket_wrapper.send(self.request, {'response': 'ok'}, self.aes_key)
                        else:
                            socket_wrapper.send(self.request, {'response': 'fail', 'reason': '账号已存在！'}, self.aes_key)
            else:
                if data['cmd'] == 'get_users':
                    userrrs = []
                    for user in file_server.clients.keys():  # 所有用户列表中遍历
                        if user != self.user:  # 若用户不是我的id，就显示在我的在线列表中传过去
                            userrrs.append(user)
                    socket_wrapper.send(self.request, {'type': 'get_users', 'data': userrrs},
                                        self.aes_key)  # 传回client的'data'为用户[]列表
                # -----------------------------------------------------------------------------------------------------------
                # 获取好友表
                # （传到client方之后 1.直接显示于弹出的框体 2.后面追加"*"表示在线好友 在线好友的获得是使用在线总表与好友表取交集）
                elif data['cmd'] == 'get_friends':
                    fris = []
                    for friend in friend_table[self.user]:  # 在我ID对应的好友list中遍历
                        if friend != self.user:  # 若好友不是我的id，就显示在我的好友表中
                            fris.append(friend)
                    socket_wrapper.send(self.request, {'type': 'get_friends', 'data': fris}, self.aes_key)

                # 添加好友
                # 在本地操作好友表 同上述获取好友表逻辑 将新list传回client端
                elif data['cmd'] == 'add':
                    friname = data['fri']
                    if add_friend(self.user, friname):
                        socket_wrapper.send(self.request, {'type': 'operation_msg', 'response': 'ok', 'msg': '添加好友成功'},
                                            self.aes_key)
                    else:
                        socket_wrapper.send(self.request,
                                            {'type': 'operation_msg', 'response': 'fail', 'msg': '好友账号不存在!'},
                                            self.aes_key)
                # 删除好友
                elif data['cmd'] == 'delete':
                    friname = data['fri']
                    if delete_friend(self.user, friname):
                        socket_wrapper.send(self.request, {'type': 'operation_msg', 'response': 'ok', 'msg': '删除好友成功!'},
                                            self.aes_key)
                    else:
                        socket_wrapper.send(self.request,
                                            {'type': 'operation_msg', 'response': 'fail', 'msg': '好友账号不存在!'},
                                            self.aes_key)
                # -----------------------------------------------------------------------------------------------------------

                elif data['cmd'] == 'get_history':
                    socket_wrapper.send(self.request, {'type': 'get_history', 'peer': data['peer'],
                                                       'data': get_history(self.user, data['peer'])}, self.aes_key)
                elif data['cmd'] == 'get_friend_ip':
                    if data['peer'] in file_server.clients:
                        socket_wrapper.send(self.request, {'type': 'get_friend_ip', 'friend_ip':
                            file_server.clients[data['peer']].client_address[0],
                                                           'peer': data['peer'], 'public_key': file_server.clients[
                                data['peer']].self_public_key}, self.aes_key)
                    else:
                        pass
                elif data['cmd'] == 'chat' and data['peer'] != '':
                    socket_wrapper.send(file_server.clients[data['peer']].request,
                                        {'type': 'msg', 'peer': self.user, 'msg': data['msg']},
                                        file_server.clients[data['peer']].aes_key)
                    append_history(self.user, data['peer'], data['msg'])
                elif data['cmd'] == 'chat' and data['peer'] == '':
                    for user in file_server.clients.keys():
                        if user != self.user:
                            socket_wrapper.send(file_server.clients[user].request,
                                                {'type': 'broadcast', 'peer': self.user, 'msg': data['msg']},
                                                file_server.clients[user].aes_key)
                    append_history(self.user, '', data['msg'])
                elif data['cmd'] == 'file_request':
                    file_server.clients[data['peer']].file_peer = self.user
                    socket_wrapper.send(file_server.clients[data['peer']].request,
                                        {'type': 'file_request', 'peer': self.user, 'filename': data['filename'],
                                         'size': data['size'], 'md5': data['md5']},
                                        file_server.clients[data['peer']].aes_key)
                elif data['cmd'] == 'file_deny' and data['peer'] == self.file_peer:
                    self.file_peer = ''
                    socket_wrapper.send(file_server.clients[data['peer']].request,
                                        {'type': 'file_deny', 'peer': self.user},
                                        file_server.clients[data['peer']].aes_key)
                elif data['cmd'] == 'file_accept' and data['peer'] == self.file_peer:
                    self.file_peer = ''
                    socket_wrapper.send(file_server.clients[data['peer']].request,
                                        {'type': 'file_accept', 'ip': self.client_address[0],
                                         'tmp_aes_key': data['tmp_aes_key']}, file_server.clients[data['peer']].aes_key)
                elif data['cmd'] == 'close':
                    self.finish()

    def finish(self):
        if self.authed:
            self.authed = False
            if self.user in file_server.clients.keys():
                del file_server.clients[self.user]
            for user in file_server.clients.keys():
                socket_wrapper.send(file_server.clients[user].request, {'type': 'peer_left', 'peer': self.user},
                                    file_server.clients[user].aes_key)


def handler_init():


if __name__ == '__main__':
    # 客户端每次运行时，初始化全局变量：从本地文件中加载用户信息及历史聊天记录
    users = load_users()
    history = load_history()
    friend_table = load_friends()

    # 接收新客户端的连接请求，递交其IP及端口号至Handler函数，建立线程
    # 在TCP协议下 完成与client线程的注册登录、好友状态及P2P聊天连接分配等功能
    app = socketserver.ThreadingTCPServer(('0.0.0.0', 8888), file_server)
    app.serve_forever()
