# -*- coding:utf-8 -*-
# @Time     :2019/10/24 0024 8:56
# @Author   :yin huajun
# @Email    :1250309341@qq.com
# @File     :test.py
# @software :PyCharm

from Netbox.DUO_test.ssh.sshconnect import commend

commend('sh /bin/reset_gemalto.sh')  # 调用脚本重启，检查之后是否识别
result = commend('lsusb')
print(result)

