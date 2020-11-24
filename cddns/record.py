'''
# @Author       : Chr_
# @Date         : 2020-11-24 14:06:27
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-24 14:47:29
# @Description  : 记录IP历史
'''

from datetime import datetime
from .log import get_logger

logger = get_logger('Record')


def get_record(path: str) -> str:
    '''
    读取IP记录
    '''
    try:
        with open(path, 'r', encoding='utf-8') as f:
            value = f.readline()
        return value or '无记录'
    except Exception as e:
        logger.error(f'读取文件失败: {e}')
        return '无记录'


def set_record(path: str, value: str) -> bool:
    '''
    保存IP记录
    '''
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(value)
        return True
    except Exception as e:
        logger.error(f'写入文件失败: {e}')
        return False
