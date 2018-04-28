# -*- coding: utf-8 -*-
# author: itimor

import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendMail(object):
    def __init__(self, MAIL_ACOUNT, sub, content, to_list, cc_list=None):
        # 设置服务器名称、用户名、密码以及邮件后缀
        self.mail_host = MAIL_ACOUNT["mail_host"]
        self.mail_user = MAIL_ACOUNT["mail_user"]
        self.mail_pass = MAIL_ACOUNT["mail_pass"]
        self.mail_postfix = MAIL_ACOUNT["mail_postfix"]
        self.sub = sub
        self.content = content
        self.to_list = to_list
        self.cc_list = cc_list

    # 发送邮件函数
    def send_mail(self):
        me = self.mail_user + "<" + self.mail_user + "@" + self.mail_postfix + ">"
        # f = open(context)
        # msg = MIMEText(f.read(),_charset="utf-8")
        # f.close()
        # msg = MIMEText(context)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.sub
        msg['From'] = me
        msg['To'] = self.to_list
        msg['Cc'] = self.cc_list
        list = msg['Cc'].split(',')
        list.append(msg['To'])
        context = MIMEText(self.content, _subtype='html', _charset='utf-8')  # 解决乱码
        msg.attach(context)
        try:
            send_smtp = smtplib.SMTP()
            send_smtp.connect(self.mail_host, 587)
            send_smtp.starttls()
            send_smtp.login(self.mail_user, self.mail_pass)

            send_smtp.sendmail(me, list, msg.as_string())
            send_smtp.close()
            return {"code": 'success', "msg": "通知邮件发送成功"}
        except Exception as e:
            print(e)
            return {"code": 'error', "msg": "通知邮件发送失败"}


if __name__ == '__main__':
    # from omsBackend.settings import MAIL_ACOUNT

    MAIL_ACOUNT = {
        "mail_host": "mail.tb-gaming.com",
        "mail_user": "oms@tb-gaming.com",
        "mail_pass": "u62En68D9d",
        "mail_postfix": "tb-gaming.com",
    }
    sub = 'aaa'
    content = 'bbb'
    to_list = 'kiven@tb-gaming.com'
    cc_list = ''
    sendmail = SendMail(MAIL_ACOUNT, sub, content, to_list, cc_list)

    if sendmail.send_mail():
        print({"code": 'success', "msg": "通知邮件发送成功"})
    else:
        print({"code": 'error', "msg": "通知邮件发送失败"})
