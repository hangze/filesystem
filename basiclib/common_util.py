# -*- coding: utf-8 -*
import os

# 获取网络磁盘基本目录，基本目录下是各个用户的目录
# @return 返回基本目录，如 C:\\User\\document:
class CommonUtil():

    @staticmethod
    def get_base_disk_dir():
        curr_dir=os.getcwd()
        return curr_dir

    @staticmethod
    def get_server_ip():
        server_ip="127.0.0.1"
        return server_ip

    @staticmethod
    def get_server_port():
        server_port=8888
        return server_port

<<<<<<< HEAD

def get_base_disk_dir():
    return None
=======
    @staticmethod
    def get_ca_private_key():
        ca_private_key='''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA2CtiLcpfJkOptfZSwB6sHxZ/Y0vxBpJM25xMnzqAbxotT/ER
sRMlEp6u5teSuJkTr4Epc2GGPWodVVpkMWQcOQFjW3AKgV3SFn8ufvAZ2Q3K8DWy
zNH97CPgg/freINiuZmPG32dkucZKtixESqpdfA4rO9ykFoHbn0QoPZXQTiVuQs3
v7uuozOnWifRU7ol5mO9CQu1I4kGy+PiphY6zjMstmUqxR0JMLRnnRo/p+91mFu4
6bxupjvoIxVj6lB+1upZZi8PPjfRPUh5BQJjPUnO+wKP3pXVP+zEVrG3krsG45lL
JENVq4i/hrFAuAiQlY5Rpt6wjD9/V7d257ye9QIDAQABAoIBABb/XJFTDZbgTXKU
m16hlL208sYBWwnQMDmP8g3hly7audXep3tvdjr6I1DfP9aAQJokE2EZT8MCYk8F
kBG6HQ+KgIPGknOLY/GtQ6jRCerv3vZ5vAUy1QEVmwnnKwe18J+ewN0Tmts5V1HZ
3lKdd4xay2jIi6dkUJSWXRnGw2cmeBxFmw5WCvUPwSPw1XcXVYBmKePd3AWR24KJ
ZNrgQV2ItIXRIxoVBlHBbgM53bNt5eIMpDSILJO7W+tUnFQ0ziqW5JyOgFA4gOHR
owMJQ2Cu/y5NEVvC2h89GJnEcWuU/GCwPpFAq0vfLeyjMdJVSf6+4kYKj/Z9nKq5
xP4O0cECgYEA4aIQtS7r58vYRF1/7ZE+TABNrYmSbQ1N4gWdWzE0YdIAmUhbh6mV
yFSPzuPUja/bY9RP6coAG+h/xVpputsy1injTCkXL1dugb2jMMmd9HGKXsxpxjmO
8uvyG4yyUUZFEBNQziaEc9vHArEhjj5bh75giMEWxFnZ06+SxEjYQzUCgYEA9UNC
rv7P5PtnwLyROGwyc1Sbf3AP00iVaNCiGvKuA0EOw/y7epUQ6wrDrnH9nP4pHXil
m3A994Vw4P0/iD2j+WufjF+AiokZvD4T3I/xAcajuyWstcAUX2kJmZDRitl5z8uf
8qj5zUaswI78patSiJGH+rT4w+g+lFtOZBuUpMECgYEAm/F12LOQSglB9KYml5wN
0VtYVHtDn2lVjcRRqEhOqtkInug6kn2rzuRa7CPcsPx9BfckMDHzd1ZukIjXkFSV
Qx16QhYYNxkXgEX/9uUx7VNXzgM7i8wWN2DJWS8Zw0Bs1Rp0e7Z1Ttn0JrEjvvrs
KdpzP7EsOhLbkQnExzKNfY0CgYBYA0EEx1AXXdiHo6OBWeJo3K3Id5BWQ6/KI0Ro
4zlq1YfU8PbeMGwXzI8YJLPcCKD8gHT9aLP0BSDSvE52N5iGQwbIOuVH0Zc4pBZA
ii70cjIDUKu/tSQacPkO8JchepVp6iqFy/mInpoTp7wmP2qos4DWiObUdp0uY+2n
ovYegQKBgCiUxztp8kfDu2f98qix6E0APjqNsVUGrOLG9cvtOwdLtAqXOzmIP4EA
DPVQegFyZ6FHrGgq7tY3HO5DvEa83FdPM1lddIqs5BG6VQ79menaJdMiatZfYIf4
D/Y5Yr5UPJ07VE5zTxg9aWvaWyUn3IsClzrA99OSOQcdtYySpTcK
-----END RSA PRIVATE KEY-----'''
        return ca_private_key

    @staticmethod
    def get_ca_public_key():
        ca_public_key='''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2CtiLcpfJkOptfZSwB6s
HxZ/Y0vxBpJM25xMnzqAbxotT/ERsRMlEp6u5teSuJkTr4Epc2GGPWodVVpkMWQc
OQFjW3AKgV3SFn8ufvAZ2Q3K8DWyzNH97CPgg/freINiuZmPG32dkucZKtixESqp
dfA4rO9ykFoHbn0QoPZXQTiVuQs3v7uuozOnWifRU7ol5mO9CQu1I4kGy+PiphY6
zjMstmUqxR0JMLRnnRo/p+91mFu46bxupjvoIxVj6lB+1upZZi8PPjfRPUh5BQJj
PUnO+wKP3pXVP+zEVrG3krsG45lLJENVq4i/hrFAuAiQlY5Rpt6wjD9/V7d257ye
9QIDAQAB
-----END PUBLIC KEY-----'''
        return ca_public_key

    @staticmethod
    def get_server_private_key():
        server_pri_key='''-----BEGIN RSA PRIVATE KEY-----
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
        return server_pri_key

    @staticmethod
    def get_server_pub_key():
        server_public_key='''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4S8MgQsMg4ckkmlyo9jz
QBPYwxz7Q9Fjuap1al3oSvqtcRx8Jndguwlk4admQoaG+3s6YAXoE8FLg+A+Nx41
344w8/tTTOr1uyd9KNCzYqyEAz5km/ZFel6gWGCTwDVjT1j2CjXhgkAOEWjvzE3e
BKhf2fLv5gDf1pvsEHca8avFkQTjpRctZUPIEvDz4cpbxYFr4naDCcplK7+FdxYN
kIUzjFS5fLUEJhM7daiJ2/NwUl1BqxVx4uPD9XiVlwhx3NhXM+hA1NtJycS3ZyM0
wa18PvHK7KB3Gryl4RRgAVxU75BRNd1ctpHklJOE9weLJqr1jlwZB3zUf2ARuZ6J
ywIDAQAB
-----END PUBLIC KEY-----'''
        return server_public_key
>>>>>>> 3f9e33cc2b221cb1d1b007f347d5910148fa4cec
