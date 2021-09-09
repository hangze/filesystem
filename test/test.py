from Crypto import Random
from Crypto.PublicKey import RSA

from basiclib.common_util import get_base_disk_dir
from basiclib.mail_util import MailServer
import smtplib
from email.mime.text import MIMEText

from client.client_ui import Login_win
from client.client_ui import Main_win

def test_mail_send():
    # todo 此处可写代码验证是否邮件能否发送成功，非必须
    # 发送邮件相关参数
    smtpserver = 'smtp.163.com'  # 发件服务器
    port = 25  # 端口
    sender = '17328618471@163.com'  # 发件人邮箱
    psw = 'EKYKJABHUUBFDJTN'  # 发件人密码
    receiver = "784985696@qq.com"  # 接收人

    # 编写邮件主题和正文，正文用的html格式
    subject = '邮件主题'
    body = '<p>这是个发送邮件的正文</p>'  # 定义邮件正文为html
    msg = MIMEText(body, 'html', 'utf-8')
    msg['from'] = sender
    msg['to'] = receiver
    msg['subject'] = subject

    # 发送邮件
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)  # 链接服务器
    smtp.login(sender, psw)  # 登录
    smtp.sendmail(sender, receiver, msg.as_string())  # 发送
    smtp.quit()  # 关闭


def test_generate_rsa_key():
    random_generator = Random.new().read
    rsa = RSA.generate(2048, random_generator)
    # 生成RSP公私钥
    private_key = rsa.exportKey().decode()  # 私钥本地生成，与公钥成对,启动时初始化
    public_key = rsa.public_key().exportKey().decode()  # 私钥本地生成，与公钥成对,启动时初始化
    print("private_key:"+private_key)
    print("public_key:" + public_key)


if __name__ == '__main__':
    # str_dir=get_base_disk_dir()
    test_generate_rsa_key()
    loginWin = Login_win()
    loginWin.show()
    mainWin = Main_win()
    mainWin.show()
