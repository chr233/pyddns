
'''
# @Author       : Chr_
# @Date         : 2020-11-23 11:47:33
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-24 12:57:04
# @Description  : 读写配置文件
'''
import toml
from collections import Iterable
from .log import get_logger

# TODO 支持cloudflare
DDNS_TYPE = {'dnspod'}

logger = get_logger('Config')


def get_config(path: str) -> dict:
    '''
    读取并验证配置
    '''
    try:
        with open(path, 'r', encoding='utf-8') as f:
            rcfg = toml.load(f)
        vcfg = __verify_config(rcfg)
        return vcfg
    except FileNotFoundError:
        logger.error(f'配置文件[{path}]不存在')
        with open(path, 'w+', encoding='utf-8') as f:
            toml.dump(__verify_config({}), f)
        logger.info('已生成默认配置,请重新运行程序')
    except ValueError as e:
        logger.error(f'配置文件验证失败 [{e}]', exc_info=True)
    return None


def __verify_config(cfg: dict) -> dict:
    '''
    验证配置
    '''
    dnspod = __v_dnspod(cfg.get('dnspod', {}))
    domains = __v_domains(cfg.get('domains', {}))
    email = __v_email(cfg.get('email', {}))
    ftqq = __v_ftqq(cfg.get('ftqq', {}))
    return {'dnspod': dnspod, 'domains': domains,
            'email': email, 'ftqq': ftqq}


def __v_dnspod(dnspod: dict) -> dict:
    token = dnspod.get('token', None)
    return {'token': token}


def __v_domains(domains: list) -> list:
    if not isinstance(domains, Iterable):
        return []

    ds = []
    for i, d in enumerate(domains, 1):
        d_name = d.get('domain', None)
        d_sub = d.get('sub', '@')
        d_type = d.get('type', 'dnspod')
        if d_name and d_sub:
            if d_type in DDNS_TYPE:
                ds.append({'domain': d_name, 'sub': d_sub, 'type': d_type})
            else:
                logger.warning(f'domains第{i}项 type 设置错误')
                logger.warning(f'type可选值为: {DDNS_TYPE}')
        else:
            logger.error(f'domains第{i}项设置错误,未设置domain或sub名称')
    return ds


def __v_email(email: dict) -> dict:
    enable = email.get('enable', False)
    port = email.get('port', 465)
    server = email.get('server', '')
    passwd = email.get('passwd', '')
    user = email.get('user', '')
    recvaddr = email.get('recvaddr', '')
    sendaddr = email.get('sendaddr', '')
    try:
        port = int(port)
    except ValueError:
        logger.warning(f'email.port必须为数字, {port}')
    return {'enable': enable,
            'server': server, 'port': port,
            'user': user, 'passwd': passwd,
            'recvaddr': recvaddr, 'sendaddr': sendaddr}


def __v_ftqq(ftqq: dict) -> dict:
    enable = ftqq.get('enable', False)
    skey = ftqq.get('skey', None)
    return {'enable': enable, 'skey': skey}
