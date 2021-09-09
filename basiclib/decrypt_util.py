import string
from Crypto import Random
from Crypto.Cipher import AES
import random
import json


# 生成aes密钥
def keyGenerater(length):
    '''''生成指定长度的秘钥'''
    if length not in (16, 24, 32):
        return None
    x = string.ascii_letters + string.digits
    return ''.join([random.choice(x) for i in range(length)])


# 待加密文本补齐到 block size 的整数倍
def PadTest(bytes):
    while len(bytes) % AES.block_size != 0:  # 循环直到补齐 AES_BLOCK_SIZE 的倍数
        bytes += ' '.encode()  # 通过补空格（不影响源文件的可读）来补齐
    return bytes  # 返回补齐后的字节列表


# AES 加密,二进制数据
def encrypt_byte(key, bytes):
    myCipher = AES.new(key.encode(), AES.MODE_ECB)  # 新建一个 AES 算法实例，使用 ECB（电子密码本）模式
    encryptData = myCipher.encrypt(PadTest(bytes))  # 调用加密方法，得到加密后的数据
    return encryptData  # 返回加密数据


# AES 解密，二进制数据
def decrypt_byte(key, encryptData):
    myCipher = AES.new(key.encode(), AES.MODE_ECB)  # 新建一个 AES 算法实例，使用 ECB（电子密码本）模式
    bytes = myCipher.decrypt(encryptData)  # 调用解密方法，得到解密后的数据
    return bytes  # 返回解密数据


# 会话过程中传输的数据 端到端使用AES算法加解密
def encrypt(data, key, encrypt_type):
    if encrypt_type == 0:
        return json.dumps({'encrypt_type': encrypt_type, 'data': data.decode()}).encode('utf-8')
    elif encrypt_type == 1:
        code = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, code)
        aes_data = code + cipher.encrypt(data)
        full_data = {'encrypt_type': encrypt_type, 'data': aes_data.decode('latin-1')}
        return json.dumps(full_data).encode('utf-8')
    elif encrypt_type == 2:
        code = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, code)
        aes_data = code + cipher.encrypt(data)
        aes_data_size = len(aes_data)
        img_data = aes_data
        full_data = {'encrypt_type': encrypt_type, 'len': aes_data_size, 'image': img_data.decode('latin-1')}
        return json.dumps(full_data).encode('utf-8')


def decrypt(data, key):
    json_data = json.loads(data)
    if json_data['encrypt_type'] == 0:
        return json_data['data']
    elif json_data['encrypt_type'] == 1:
        real_data_tmp = json_data['data']
        real_data = real_data_tmp.encode('latin-1')
        return AES.new(key, AES.MODE_CFB, real_data[:16]).decrypt(real_data[16:])
    elif json_data['encrypt_type'] == 2:
        real_data_tmp = json_data['image']
        aes_data_size = json_data['len']
        img_data = real_data_tmp.encode('latin-1')
        real_data = img_data
        return AES.new(key, AES.MODE_CFB, real_data[:16]).decrypt(real_data[16:])

#todo 请求的相关数据，对其进行签名，返回签名结果
def signture(ip_addr:str, pad_data:str ,pri_key:str):
    pass
