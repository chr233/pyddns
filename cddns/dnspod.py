
'''
# @Author       : Chr_
# @Date         : 2020-11-24 00:25:31
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-24 14:37:19
# @Description  : DNSPOD API
'''

from logging import raiseExceptions
from typing import IO
import requests
from .log import get_logger
logger = get_logger('Dnspod')

DOMAINS = {}
SUBS = {}


def __basic_request(token: str, url: str, data: dict = None):
    '''
    封装DnspodAPI请求
    '''
    d = {'login_token': token,
         'format': 'json',
         'lang': 'cn',
         **(data or {})}
    h = {'User-Agent': 'curl/7.29.0'}
    resp = None
    try:
        resp = requests.post(url=url, data=d, headers=h)
        jd = resp.json()
        return jd
    except Exception as e:
        logger.error(
            f'API ERROR {e}\ninfo:\n{resp.text if resp else "No info"}')


def change_ip(dnspodcfg: str, domain: str, sub: str, value: str) -> bool:
    '''
    修改记录,返回是否成功
    '''
    global DOMAINS
    global SUBS

    token=dnspodcfg.get('token')

    if domain in DOMAINS:
        d_id = DOMAINS.get(domain)
    else:
        DOMAINS.update(get_domain_list(token))
        d_id = DOMAINS.get(domain)
    if not d_id:
        logger.error(f'域名{domain}不存在')
        return False
    if sub in SUBS:
        r = SUBS.get(sub)
    else:
        SUBS.update(get_record_list(token, d_id))
        r = SUBS.get(sub)
    if not r:
        logger.info(f'子域名{sub}不存在')
        result = add_record(token, d_id, sub, value, 0)
        logger.info(f'添加解析记录{sub}.{domain} = {value}')
    else:
        r_id, r_value, r_line = r
        if r_value == value:
            logger.info(f'子域名{sub}.{domain}记录值无需更改')
            return True
        result = set_record(token, d_id, r_id, sub, value, r_line)
        logger.info(f'修改解析记录{sub}.{domain} = {r_value} --> {value}')
    logger.info('成功' if result else '失败')
    return result


def get_domain_list(token: str) -> dict:
    '''
    获取域名字典 {域名:域名ID}
    '''
    url = 'https://dnsapi.cn/Domain.List'

    jd = __basic_request(token, url)
    if jd:
        domains = {}
        for d in jd.get('domains', {}):
            d_id = d.get('id', 0)
            d_name = d.get('name', 'Error')
            domains[d_name] = d_id
        return domains
    else:
        logger.error('获取域名列表出错')


def get_record_list(token: str, d_id: int) -> dict:
    '''
    获取域名记录字典 {子域名:子域名ID,子域名记录,子域名线路}
    '''
    url = 'https://dnsapi.cn/Record.List'
    data = {'domain_id': d_id, 'record_type': 'A'}

    jd = __basic_request(token, url, data)
    if jd:
        records = {}
        for r in jd.get('records', {}):
            r_id = r.get('id', 0)
            r_name = r.get('name', 'Error')
            r_value = r.get('value', None)
            r_lineid = r.get('line_id', 0)
            records[r_name] = (r_id, r_value, r_lineid)
        return records
    else:
        logger.error('获取域名记录列表出错')


def add_record(token: str, d_id: int, sub: str, value: str, line_id: int = 0) -> bool:
    '''
    添加域名解析记录 
    '''
    url = 'https://dnsapi.cn/Record.Create'
    data = {'domain_id': d_id,
            'sub_domain': sub, 'record_type': 'A',
            'value': value, 'ttl': 600,
            'record_line_id': line_id}

    jd = __basic_request(token, url, data)
    if jd:
        success = jd.get('status', {}).get('code', None) == '1'
        return success
    else:
        logger.error('添加域名记录出错')
        return False


def set_record(token: str, d_id: int, r_id: int, sub: str, value: str, line_id: int = 0) -> bool:
    '''
    修改域名解析记录
    '''
    url = 'https://dnsapi.cn/Record.Modify'
    data = {'domain_id': d_id, 'record_id': r_id,
            'sub_domain': sub, 'record_type': 'A',
            'value': value, 'ttl': 600,
            'record_line_id': line_id}

    jd = __basic_request(token, url, data)
    if jd:
        success = jd.get('status', {}).get('code', None) == '1'
        return success
    else:
        logger.error('修改域名记录出错')
        return False
