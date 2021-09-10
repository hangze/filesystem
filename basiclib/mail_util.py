import smtplib
from email.mime.text import MIMEText


class MailServer:
    # todo 此处去临时申请一个163mail，并开启stmp，搜索python+163+发送邮件
    admin_mail = "17328618471@163.com" #管理员邮箱
    admin_pwd = "EKYKJABHUUBFDJTN" #管理员邮箱Key
    smtpserver = 'smtp.163.com'  # 发件服务器
    port = 25  # 端口

    # todo #此处向指定邮箱des_mail_addr发送验证码
    def send_verify_mail(self, verify_code: str, des_mail_addr):
        # 发送邮件
        # 发送邮件相关参数
        receiver = des_mail_addr  # 接收人

        # 编写邮件主题和正文，正文用的html格式
        subject = '邮件主题'
        body = f'<p>your verify code is {verify_code}</p>'  # 定义邮件正文为html
        msg = MIMEText(body, 'html', 'utf-8')
        msg['from'] = self.admin_mail
        msg['to'] = receiver
        msg['subject'] = subject

        smtp = smtplib.SMTP()
        smtp.connect(self.smtpserver)  # 链接服务器
        smtp.login(self.admin_mail, self.admin_pwd)  # 登录
        smtp.sendmail(self.admin_mail, des_mail_addr, msg.as_string())  # 发送
        smtp.quit()  # 关闭
        return True
