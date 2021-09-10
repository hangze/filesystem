import base64

from basiclib.common_util import CommonUtil
from basiclib.crypt_util import create_signture
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher


class SecurityService:
    ca_book_dict = dict()
    private_cipher = None

    def __init__(self):
        # 初始化ca_book
        ca_book_dict = dict()
        ca_book_dict["server_ip"] = CommonUtil.get_server_ip()
        ca_book_dict["server_port"] = CommonUtil.get_server_port()
        ca_book_dict["server_pub_key"] = CommonUtil.get_server_pub_key()
        str_signture = create_signture(ca_book_dict, CommonUtil.get_ca_public_key())
        ca_book_dict["signture"] = str(str_signture,encoding="utf-8")
        self.ca_book_dict = ca_book_dict

        # 初始化密钥解析器
        self.private_cipher = PKCS1_cipher.new(RSA.importKey(CommonUtil.get_server_private_key()))

    def get_ca_book(self):
        return self.ca_book_dict

    def decrypt_data(self, data: str):
        decrypt_data = self.private_cipher.decrypt(base64.b64decode(data), 0)
        return decrypt_data
