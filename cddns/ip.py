
'''
# @Author       : Chr_
# @Date         : 2020-11-23 17:16:08
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-24 10:55:21
# @Description  : 获取当前IP
#                 部分参考 https://github.com/strahe/dnspod-ddns
'''

import re
import requests
from .log import get_logger

logger = get_logger('getip')

HEADERS = {'User-Agent': 'curl/7.29.0'}

REGEX_IP = re.compile((
    r'\D*('
    r'(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.'
    r'(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.'
    r'(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.'
    r'(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)'
    r')\D*'))


def get_ip():
    '''
    多种方式读取IP
    '''
    return (__get_ip_by_ipip()
            or __get_ip_by_ipcn()
            or __get_ip_by_cip()
            or __get_ip_by_httpbin())


def __regex_match(input: str):
    '''
    正则读取IP
    '''
    try:
        result = REGEX_IP.match(input).group(1)
        return result
    except Exception as e:
        logger.warning(f'匹配IP失败: {e}')
        logger.warning(f'输入内容:\n{input}')
        return None


def __get_ip_by_ipip():
    url = 'https://myip.ipip.net/'
    try:
        resp = requests.get(url=url, headers=HEADERS, timeout=10)
        return __regex_match(resp.content.decode('utf-8'))
    except Exception as e:
        logger.warning(f'get_ip_by_ipip FAILED: {e}')
        return None


def __get_ip_by_ipcn():
    url = 'https://ip.cn/api/index?ip=&type=0'
    try:
        resp = requests.get(url=url, headers=HEADERS, timeout=10)
        return __regex_match(resp.content.decode('utf-8'))
    except Exception as e:
        logger.warning(f'get_ip_by_ipcn FAILED: {e}')
        return None


def __get_ip_by_cip():
    url = 'https://www.cip.cc/'
    try:
        resp = requests.get(url=url, headers=HEADERS, timeout=10)
        return __regex_match(resp.content.decode('utf-8'))
    except Exception as e:
        logger.warning(f'get_ip_by_cip FAILED: {e}')
        return None


def __get_ip_by_httpbin():
    url = 'https://www.httpbin.org/ip'
    try:
        resp = requests.get(url=url, headers=HEADERS, timeout=10)
        return __regex_match(resp.content.decode('utf-8'))
    except Exception as e:
        logger.warning(f'get_ip_by_httpbin FAILED: {e}')
        return None
