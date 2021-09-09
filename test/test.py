from basiclib.common_util import get_base_disk_dir
from basiclib.mail_util import MailServer


def test_mail_send():
    # todo 此处可写代码验证是否邮件能否发送成功，非必须
    test_mail_addr = "276095361@qq.com"
    mail_content = str.format('your verify code is %s', "123456")
    mail_server = MailServer()
    mail_server.send_verify_mail(mail_content, test_mail_addr)


if __name__ == '__main__':
  #  str_dir=get_base_disk_dir()
    test_mail_send()
