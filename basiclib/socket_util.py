import struct
import json

from basiclib.crypt_util import encrypt, decrypt

max_buff_size = 1024  # 单次最大传输数据大小


# pack函数：待发送的数据，首先与其大小（二进制长度）连接打包
# 则接收时，先获取到数据包大小，然后接收此长度的二进制数据
def pack(data):
    return struct.pack('>L', len(data)) + data


# 使用socket收-发数据
def send(socket, data_dict, key):
    socket.send(pack(encrypt(json.dumps(data_dict).encode('utf-8'), key, 1)))


# 使用socket收-发数据,不加密
def raw_send(socket, data_dict):
    socket.send(pack(encrypt(json.dumps(data_dict).encode('utf-8'), '', 0)))


def recv(socket, key):
    data = b''
    surplus = struct.unpack('>L', socket.recv(4))[0]
    socket.settimeout(5)
    while surplus:
        recv_data = socket.recv(max_buff_size if surplus > max_buff_size else surplus)
        data += recv_data
        surplus -= len(recv_data)
    socket.settimeout(None)
    return json.loads(decrypt(data, key))


# 使用socket收-发数据,不加密
def raw_recv(socket):
    data = b''
    surplus = struct.unpack('>L', socket.recv(4))[0]
    socket.settimeout(5)
    while surplus:
        recv_data = socket.recv(max_buff_size if surplus > max_buff_size else surplus)
        data += recv_data
        surplus -= len(recv_data)
    socket.settimeout(None)
    return json.loads(data)
