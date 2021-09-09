from basiclib.common_util import CommonUtil
from basiclib.crypt_util import create_signture


class SecurityService:
    ca_book_dict = dict()

    def __init__(self):
        ca_book_dict = dict()
        ca_book_dict["server_ip"] = CommonUtil.get_server_ip()
        ca_book_dict["server_port"] = CommonUtil.get_server_port()
        ca_book_dict["server_pub_key"]=CommonUtil.get_server_pub_key()
        str_signture = create_signture(ca_book_dict, CommonUtil.get_ca_private_key())
        ca_book_dict["signture"] = str_signture
        self.ca_book_dict = ca_book_dict

    def get_ca_book(self):
        return self.ca_book_dict
