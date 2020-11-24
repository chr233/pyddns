'''
# @Author       : Chr_
# @Date         : 2020-11-24 12:12:01
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-24 17:49:24
# @Description  : 打印日志
'''

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s : %(message)s',
                    datefmt='%H:%M:%S')


def get_logger(tag: str = 'Null') -> logging.Logger:
    '''
    获取logger对象
    '''
    return(logging.getLogger(tag))