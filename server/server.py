import base64
import socketserver
from typing import Any

from Crypto.PublicKey import RSA

from basiclib import socket_util
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

from basiclib.common_util import CommonUtil


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
                if data['cmd'] == 'get_private_key':
                    public_key = data['public_key']
                    pub_key = RSA.importKey(public_key)
                    self.self_public_key = public_key
                    cipher = PKCS1_cipher.new(pub_key)
                    aes_key = socket_util.keyGenerater(16)
                    self.aes_key = aes_key.encode()
                    encrypt_aes_key = base64.b64encode(cipher.encrypt(bytes(aes_key.encode("utf8"))))
                    socket_util.raw_send(self.request, {'response': 'ok', 'aes_key': encrypt_aes_key.decode()})
                else:
                    self.user = data['user']
                    if data['cmd'] == 'login':  # 本地实现登录请求
                        if validate(data['user'], data['pwd']):
                            socket_util.send(self.request, {'response': 'ok'}, self.aes_key)
                            self.authed = True
                            for user in file_server.clients.keys():
                                socket_util.send(file_server.clients[user].request,
                                                 {'type': 'peer_joined', 'peer': self.user},
                                                 file_server.clients[user].aes_key)
                            file_server.clients[self.user] = self
                        else:
                            socket_util.send(self.request, {'response': 'fail', 'reason': '账号或密码错误！'}, self.aes_key)
                    elif data['cmd'] == 'register':
                        if register(data['user'], data['pwd']):
                            socket_util.send(self.request, {'response': 'ok'}, self.aes_key)
                        else:
                            socket_util.send(self.request, {'response': 'fail', 'reason': '账号已存在！'}, self.aes_key)
            else:
                if data['cmd'] == 'get_users':
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


server_private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA4S8MgQsMg4ckkmlyo9jzQBPYwxz7Q9Fjuap1al3oSvqtcRx8
Jndguwlk4admQoaG+3s6YAXoE8FLg+A+Nx41344w8/tTTOr1uyd9KNCzYqyEAz5k
m/ZFel6gWGCTwDVjT1j2CjXhgkAOEWjvzE3eBKhf2fLv5gDf1pvsEHca8avFkQTj
pRctZUPIEvDz4cpbxYFr4naDCcplK7+FdxYNkIUzjFS5fLUEJhM7daiJ2/NwUl1B
qxVx4uPD9XiVlwhx3NhXM+hA1NtJycS3ZyM0wa18PvHK7KB3Gryl4RRgAVxU75BR
Nd1ctpHklJOE9weLJqr1jlwZB3zUf2ARuZ6JywIDAQABAoIBAEbyM9ZUTNUDtxoJ
7vyAVeNSXXDbqK5tQiY09llUzOMSp6KDfvn/kpJbG1WdEDLVf6Gr6XBna/8NX2Vl
OTTUZ9TPT80O2efZ/yHAB0bcuifUgqMi/T/GD43GUm6FvwdHysotFReSckI/PC9w
CF0uC00cX1ajm8GzdNKAvZdSb0LEbGaByc2Uqb37wf6M4633I71JejAxcKUvXm78
JjmR9rgpsN3rB/gLz20TAdTkLeVdRw9YbKj+BztaHIBo9wNKK95RDONFe4gjUCF+
gU0aBS64bsMmCZzowsgkTxNt48VA+PZcRL28IQp8I4fFiSHx07tJyoi+//99iqcg
Jq8wgUECgYEA7jCm4i7WYN1c+goWaC5KTVPnDdOzELWclxV14btzZjTQFuZrjeRU
K2VGbL/XdEHQzkuECN7A7u9MjZjIYIOKfzgiDsXbQtHcOzOC4dbpnvG97rG4upar
KXVOj0X94mQ/G170uSXweccShe9lvm5r0PrGvGlO7ZGk61E+e8g3cY0CgYEA8gVv
js9w0ERi/IY9NV+nHV2zd9NOTA9X6hP5brJPPAMhA48MtIiPkexQC2ndWVPF1ryQ
d/ZaEC0Av5rPdUvQrgAZ04jmnzgTSaR1LZidVp8RAowShT1uBFYXm4TO/LtOpEw0
GqpyaA+R181vbPmLfU6JytFrFwvxYAv58DXzVrcCgYBHS/bYI072RayMB7L3UkvZ
Y7D4uZKTANmze7ACdpqvUEWtZSFyopLzPmhbKv1yBjVbWs1V3l9/5c9TXxUzloxB
UmsXYvAjyy+R5PRbZ3ocop3IshfqeikXys5OIpRBTOJ67exw80NNIGKSBru8yc6q
CjastRT0FbF44qPCZ4b5DQKBgQDSRf7C6WBu0rveAxOzB8Q+M2b2ONTSKJKNgYU5
tBo7XcyVNvgm8m8qrVJuWDBEqBA/nd03HQbq/u6jinGsy44nX1cQ/uTAeQvo88YL
M4mf9NvmhqSgttqbUeF48U6VLngJL1wlvulfmAdyo76nw7h5yn7VhFWy1GGGvWEO
XxFoyQKBgBFWyDcapEaC25rPRsgCJfgVZIzYzDefFvsbway1Z8utboC5LOPWUqki
LVLjDC0Lud8mQqVuHdjdpc9q2bDSfVe14uTm3h4R5s0cGsRps0Rah5Q25mM3ZAsi
juut+tE/tGFSLrO9kGwPX9875cqy3nB7CiZGghPh+Jl+fOCXWX79
-----END RSA PRIVATE KEY-----'''

server_public_key = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4S8MgQsMg4ckkmlyo9jz
QBPYwxz7Q9Fjuap1al3oSvqtcRx8Jndguwlk4admQoaG+3s6YAXoE8FLg+A+Nx41
344w8/tTTOr1uyd9KNCzYqyEAz5km/ZFel6gWGCTwDVjT1j2CjXhgkAOEWjvzE3e
BKhf2fLv5gDf1pvsEHca8avFkQTjpRctZUPIEvDz4cpbxYFr4naDCcplK7+FdxYN
kIUzjFS5fLUEJhM7daiJ2/NwUl1BqxVx4uPD9XiVlwhx3NhXM+hA1NtJycS3ZyM0
wa18PvHK7KB3Gryl4RRgAVxU75BRNd1ctpHklJOE9weLJqr1jlwZB3zUf2ARuZ6J
ywIDAQAB
-----END PUBLIC KEY-----'''

if __name__ == '__main__':
    # 服务端每次运行时，加载用户列表、群组列表
    # todo

    # 接收新客户端的连接请求，递交其IP及端口号至Handler函数，建立线程
    # 在TCP协议下 完成与client线程的注册登录、好友状态及P2P聊天连接分配等功能
    server_port = CommonUtil.get_server_port()
    app = socketserver.ThreadingTCPServer(('0.0.0.0', server_port), file_server)
    app.serve_forever()
