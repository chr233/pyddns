# CDDNS

支持Dnspod, 自动更新IP

## 开始使用

1. 安装 `pip install cddns` 或者 `clone https://github.com/chr233/pyddns`

2. 修改配置文件,填写域名和dnspod API token

    ```toml
    [dnspod]
    token = ''

    [[domains]]
    domain = 'chrxw.com'
    sub = 'test'
    ```

    完整配置参考[example.config.toml][0]

3. 运行 `python3 ddns.py`

    或者自己调用 `cddns.ddns`:

    ```python
    from cddns import ddns
    ddns('config.toml', 'ip.txt') # 自行修改配置文件路径
    ```

4. 建议使用 `corntab` 来定时运行

   例如每30分钟运行一次:

   ```txt
   */30 * * * * python3 /root/ddns/ddns.py > /dev/null 2>&1 &
   ```

5. 更新脚本方法: `pip3 install cddns --upgrade`

[0]: https://github.com/chr233/pyddns/blob/main/example.config.toml
