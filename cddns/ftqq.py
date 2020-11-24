'''
# @Author       : Chr_
# @Date         : 2020-11-24 10:25:20
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-24 10:54:20
# @Description  : 发送方糖气球推送
'''

import requests
from .log import get_logger
logger = get_logger('Ftqq')


def send_ftqq(desc: str, ftqqcfg: dict) -> bool:
    '''
    发送方糖气球推送
    '''
    if not ftqqcfg.get('enable', False):
        return False
    skey = ftqqcfg.get('skey', None)
    url = f'https://sc.ftqq.com/{skey}.send'
    d = {'text': '你的IP已变更',
         'desp': str(desc)}
    resp = requests.post(url=url, data=d)
    try:
        jd = resp.json()
        code = int(jd.get('errno', 1))
        if code == 0:
            logger.debug('FTQQ推送成功')
            return True
        else:
            msg = jd.get('errmsg', '空')
            logger.error(f'FTQQ推送失败: {msg}')
            return False
    except Exception as e:
        logger.error(f'FTQQ推送失败: {e}')
        return False
