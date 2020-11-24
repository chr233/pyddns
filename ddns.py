#!/usr/bin/python3
'''
# @Author       : Chr_
# @Date         : 2020-11-24 01:15:30
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-24 14:55:22
# @Description  : 启动文件
'''

from cddns import ddns
from os import path

SCRIPT_PATH = path.split(path.realpath(__file__))[0]
CONFIG_PATH = path.join(SCRIPT_PATH, 'config.toml')
CACHE_PATH = path.join(SCRIPT_PATH, 'ip.txt')


ddns(CONFIG_PATH, CACHE_PATH)
