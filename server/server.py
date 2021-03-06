import socketserver
from typing import Any

from basiclib import socket_util

from basiclib.common_util import CommonUtil
from security_service import SecurityService
from basiclib.file_service import FileService
from user_service import UserService

security_service = SecurityService()
user_service = UserService()
file_service = FileService()
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
        global user_service
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
                    try:
                        user_email = user_service.get_user_email(user_name)
                        user_service.retrive_pwd(user_name=user_name, user_email=user_email)
                        socket_util.send(self.request, {'type': 'retrieve_pwd_rsp','user_name':user_name,'response': 'ok', 'msg': '验证码发送成功'},
                                         self.aes_key)
                    except Exception as e:
                        socket_util.send(self.request,
                                         {'type': 'retrieve_pwd_rsp', 'response': 'fail', 'msg': str(e)},
                                         self.aes_key)

                elif data["type"] == "retrieve_pwd_verify_code":
                    user_name = data["user_name"]
                    user_new_pwd = data["new_pwd"]
                    verify_code = data["verify_code"]
                    try:
                        user_service.retrive_pwd_verify(user_name=user_name, user_new_pwd=user_new_pwd,
                                                        verify_code=verify_code)
                        socket_util.send(self.request, {'type': 'operation_msg', 'response': 'ok', 'msg': '密码重置成功'},
                                         self.aes_key)
                    except Exception as e:
                        socket_util.send(self.request,
                                         {'type': 'operation_msg', 'response': 'fail', 'msg': str(e)},
                                         self.aes_key)


                elif data["type"] == "register":
                    user_name = data["user_name"]
                    user_pwd = data["user_pwd"]
                    user_email = data["user_email"]
                    try:
                        user_service.register(user_name=user_name, user_pwd=user_pwd, user_email=user_email)
                        socket_util.send(self.request, {'type': 'operation_msg', 'response': 'ok', 'msg': '注册成功'},
                                         self.aes_key)
                    except Exception as e:
                        socket_util.send(self.request, {'type': 'operation_msg', 'response': 'fail', 'msg': '注册失败'},
                                         self.aes_key)
                        raise e
                        print(e)

                elif data["type"] == "login":
                    user_name = data["user_name"]
                    user_pwd = data["user_pwd"]
                    try:
                        token = user_service.login(user_name, user_pwd)
                        socket_util.send(self.request,
                                         {'type': 'login_result', 'response': 'ok', 'token': token, 'msg': '认证成功'},
                                         self.aes_key)
                    except Exception as e:
                        socket_util.send(self.request, {'type': 'login_result', 'response': 'fail', 'msg': str(e)},
                                         self.aes_key)
                        # -----------------------------------------------------------------------------------------------------------
                elif data['token'] == '':
                    socket_util.send(self.request, {'type': 'operation_msg', 'response': 'fail','msg': "请登录"}, self.aes_key)
                else:
                    # 验证token是否有效
                    if user_service.is_login(token):
                        if data["type"] == "get_my_space":
                            user_name = data["user_name"]
                            file_list = file_service.ger_user_file_list(user_name)
                            socket_util.send(self.request,
                                             {'type': 'get_my_space_rsp', 'file_list': file_list, 'response': 'ok'},
                                             self.aes_key)
                        elif data["type"] == "get_group_space":
                            user_name = data["user_name"]
                            group_name = data["group_name"]
                            try:
                                user_service.is_group_member(user_name,group_name)
                                file_list = file_service.ger_user_file_list(group_name)
                                socket_util.send(self.request,
                                                 {'type': 'get_my_space_rsp', 'file_list': file_list, 'response': 'ok'},
                                                 self.aes_key)
                            except Exception as e:
                                socket_util.send(self.request,
                                                 {'type': 'get_my_space_rsp', 'file_list': file_list,
                                                  'response': 'fail'},
                                                 self.aes_key)


                        elif data["type"] == "get_my_group":
                            user_name = data["user_name"]
                            group_list = user_service.get_user_group(user_name)
                            socket_util.send(self.request,
                                             {'type': 'get_my_group_rsp', 'group_list': group_list, 'response': 'ok'},
                                             self.aes_key)

                        elif data["type"] == "download_file":
                            user_name= data["user_name"]
                            file_path = data["file_path"]
                            file_name = data["file_name"]
                            aes_key = data["aes_key"]
                            net_port = data["net_port"]
                            net_ip=self.client_address[0]
                            FileService.upload_file(net_ip,net_port,aes_key,file_path)
                        elif data["type"] == "upload_file":
                            user_name= data["user_name"]
                            file_path = data["file_path"]
                            file_name = data["file_name"]
                            aes_key = data["aes_key"]
                            net_port = data["net_port"]
                            file_md5=data["file_md5"]
                            is_group_space=data["is_group_space"]
                            try:
                                if is_group_space:
                                    group_name=data["group_name"]
                                    user_service.is_group_member(user_name, group_name)
                                    base_dir = FileService.get_user_disk_dir(group_name)
                                else:
                                    base_dir = FileService.get_user_disk_dir(user_name)
                                file_full_path=base_dir+"\\"+file_path+file_name
                                FileService.listen_download_file(net_port,aes_key,file_full_path,file_name,file_md5,False)
                            except Exception as e:
                                socket_util.send(self.request,
                                                 {'type': 'operation_msg', 'response': 'fail', 'msg': str(e)},
                                                 self.aes_key)
                        elif data["type"] == "add_group":
                            user_name= data["user_name"]
                            group_name = data["group_name"]
                            group_key = data["group_key"]
                            try:
                                user_service.user_add_group(user_name,group_name,group_key)
                                socket_util.send(self.request, {'type': 'operation_msg','response': 'ok', 'msg': "新增或加入群组成功"},
                                                 self.aes_key)
                            except Exception as e:
                                socket_util.send(self.request, {'type': 'operation_msg', 'response': 'fail','msg': "新增或加入群组失败"},
                                                 self.aes_key)



                    else:
                        socket_util.send(self.request, {'type': 'operation_msg','response': 'fail', 'msg': "token无效，请重新登录"}, self.aes_key)

    def finish(self):
        if self.authed:
            self.authed = False
            if self.user in file_server.clients.keys():
                del file_server.clients[self.user]


def handler_init():
    global hanler_dict
    # hanler_dict["get_file_list"] =


if __name__ == '__main__':
    # 服务端每次运行时，加载用户列表、群组列表
    # 接收新客户端的连接请求，递交其IP及端口号至Handler函数，建立线程
    server_port = CommonUtil.get_server_port()
    app = socketserver.ThreadingTCPServer(('0.0.0.0', server_port), file_server)
    app.serve_forever()
