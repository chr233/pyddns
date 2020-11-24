'''
# @Author       : Chr_
# @Date         : 2020-11-24 10:25:17
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-24 13:01:40
# @Description  : 发送电子邮件推送
'''

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from .log import get_logger

logger = get_logger('Email')


def send_email(message: str, emailcfg: dict) -> bool:
    '''
    发送消息到电子邮箱

    参数:
        title: 标题
        text: 内容
        emailcfg: 电邮配置
    返回:
        bool: 是否成功
    '''
    enable = emailcfg.get('enable',False)
    if not enable:
        return False
    mailobj = MIMEMultipart()
    sendaddr = emailcfg.get('sendaddr')
    recvaddr = emailcfg.get('recvaddr')
    server = emailcfg.get('server')
    port = emailcfg.get('port')
    user = emailcfg.get('user')
    passwd = emailcfg.get('passwd')
    mailobj['From'] = formataddr(["CDDNS邮件提醒", sendaddr])
    mailobj['To'] = Header(recvaddr, 'utf-8')
    mailobj['Subject'] = Header('你的IP已变更', 'utf-8')
    mailobj.attach(MIMEText(message, 'plain', 'utf-8'))
    try:
        with smtplib.SMTP_SSL(host=server, port=port) as smtpObj:
            smtpObj.connect(host=server, port=port)
            smtpObj.login(user=user, password=passwd)
            smtpObj.sendmail(sendaddr, recvaddr, mailobj.as_string())
        logger.debug('邮件发送成功')
        return True
    except Exception as e:
        logger.error(f'发送邮件失败: {e}')
        return False

