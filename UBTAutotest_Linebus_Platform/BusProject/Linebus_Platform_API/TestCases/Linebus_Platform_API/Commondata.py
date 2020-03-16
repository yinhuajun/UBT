# -*- coding:utf-8 -*-
# @Time     :2019/4/8 10:12
# @Author   :YIN
# @Email    :649626809@qq.com
# @File     :Commondata.py
# @software :PyCharm

import time
from BusProject.Linebus_Platform_API.common.Request_API import ApiRequests
from BusProject.Linebus_Platform_API.common.read_mysql import operation_mysql
from BusProject.Linebus_Platform_API.common import DataPaths
import hashlib
import datetime
from faker import Faker


class CommonData:
    # 接口的url
    url = ""

    # 用来测试的租户id
    tid = ''

    # tid='305022698075984384'
    channel_id = ''

    # ticketing platform 的userid
    operatorid = ""

    # 从数据库获取票务平台后台的usernam,password
    bsp_user_username = None
    bsp_user_password = None

    # 获取票务平台后台的operatortoken
    operatortoken = None

    # website用户的account,password
    user_account = "+8615011111111"
    user_password = "a123456"

    # 当前时间戳
    current_time = str(int(time.time()))

    # faker设置国家
    f = Faker(locale='zh_CN')
    fu = Faker('en_US')

    # 开始结束时间戳
    start = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d'))) * 1000
    next_seven_day = datetime.date.today() + datetime.timedelta(days=7)
    end = int(time.mktime(time.strptime(str(next_seven_day), '%Y-%m-%d'))) * 1000

    # type是0的tid
    type_tid = None

    # 设置busline
    buslineId = None

    # dateType
    # 产生随机dateType
    dateType = 'day'

    # linbus_name
    linebus_name = None

    # pageNo,pageSize
    pageNo = None
    pageSize = None

    # sortProperties   sortDirection
    sortProperties = 'USERNAME'
    sortDirection = 'ASC'

    # 生成email
    email = fu.ascii_email()

    # name生成名字随机值
    firstName = fu.first_name()
    lastName = fu.last_name()
    allName = firstName + lastName

    # password生成一个密码
    password = fu.password()

    # phone有关电话号码的随机值
    purePhone = f.phone_number()
    phone = '+86' + purePhone

    # Content-Type
    Content_Type = 'application/x-www-form-urlencoded'

    # 存储username，access_token
    username = None
    access_token = None
    username_password = None
