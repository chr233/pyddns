'''
# @Author       : Chr_
# @Date         : 2020-11-24 14:51:48
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-24 14:58:48
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
    description="用Python实现的小黑盒客户端",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chr233/pyxiaoheihe",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'pyDes',
        'rsa'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ),
)
