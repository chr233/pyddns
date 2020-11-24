
'''
# @Author       : Chr_
# @Date         : 2020-11-24 01:18:01
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-24 14:49:49
# @Description  : 包文件
'''

from collections import Iterable
from re import T
from .config import get_config
from .log import get_logger
from .ip import get_ip
from .dnspod import change_ip
from .record import get_record, set_record
from .email import send_email
from .ftqq import send_ftqq

VERSION = 0.1

logger = get_logger('CDNS')


def ddns(cfg_path: str, cache_path: str) -> bool:
    '''
    启动入口
    '''
    ip = get_ip()
    last_ip = get_record(cache_path)

    if ip == last_ip:
        logger.info('IP未改变,结束')
        return True

    message = f'原IP/新IP: {last_ip} -> {ip}'
    logger.info(f'IP已更新,{message}')

    cfg = get_config(cfg_path)
    if not cfg:
        logger.error('读取配置文件失败,程序退出')
        raise ValueError('读取配置文件失败')

    domains = cfg.get('domains')
    if isinstance(domains, Iterable):
        d_cfg = cfg.get('dnspod', {})
        for domain in domains:
            d_name = domain.get('domain')
            d_sub = domain.get('sub')
            change_ip(d_cfg, d_name, d_sub, ip)
    else:
        logger.error('domains配置无效')
        raise ValueError('domains配置无效')

    set_record(cache_path, ip)

    ftqq_cfg = cfg.get('ftqq', {})
    email_cfg = cfg.get('email', {})

    logger.info('发送推送')
    send_ftqq(message, ftqq_cfg)
    send_email(message, email_cfg)
    logger.info('执行结束')
    return True
