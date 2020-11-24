'''
# @Author       : Chr_
# @Date         : 2020-11-24 14:51:48
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-24 15:02:53
# @Description  : 打包文件
'''

import setuptools
from cddns import VERSION

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="cddns",
    version=VERSION,
    author="Chr_",
    author_email="chr@chrxw.com",
    description="支持多域名的ddns脚本",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chr233/pyddns",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'toml'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ),
)
