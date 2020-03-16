# -*- coding:utf-8 -*-
# @Time     :2019/6/10 10:17
# @Author   :yinhuajun
# @Email    :wangying@riverroad.cn
# @File     :test_salesreport_buslinedetailsales.py
# @software :PyCharm
import unittest
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs
from BusProject.Linebus_Platform_API.common.read_datas import ReadDatas
from BusProject.Linebus_Platform_API.common import DataPaths
from ddt import ddt, data
from BusProject.Linebus_Platform_API.common.Request_API import ApiRequests
from BusProject.Linebus_Platform_API.TestCases.Linebus_Platform_API.Commondata import CommonData as CD
from BusProject.Linebus_Platform_API.common.Data_Re import DataRe
from BusProject.Linebus_Platform_API.common.output_log import output
from BusProject.Linebus_Platform_API.common.read_mysql import operation_mysql
import time
import hashlib
import requests

testdata = ReadDatas(DataPaths.DatasPath).read_datas("ucss_a_inactive")


@ddt
class Ucss_a_inactive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log = MyLogs()
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.re = DataRe()
        cls.api = ApiRequests()

    def setUp(self):
        self.log.info("开始测试")
        if CD.bsp_user_username is None:
            bsp_user = operation_mysql("select * from bus_bsp.bsp_user where tenant_id = \'" + CD.tid + "\';")
            setattr(CD, 'bsp_user_username', bsp_user[0]["username"])
            setattr(CD, 'bsp_user_password', bsp_user[0]["password"])
        if CD.username is None:
            name = operation_mysql("SELECT username,password FROM bus_bsp.bsp_user LIMIT 1")[0]
            setattr(CD, 'username', name["username"])
            setattr(CD, 'username_password', name['password'])
            tokenname = name["username"] + 'ucss_account'
            actoken = hashlib.md5(tokenname.encode(encoding='UTF-8')).hexdigest()
            setattr(CD, 'access_token', actoken)

    def tearDown(self):
        self.log.info("结束测试")
        setattr(CD, 'current_time', str(int(time.time())))

    @classmethod
    def tearDownClass(cls):
        pass

    @data(*testdata)
    def test_ucss_a_inactive(self, datas):
        datas['url'] = self.re.url_re(datas['path'])
        datas['header'] = eval(self.re.param_re(datas['header']))
        datas['param'] = eval(self.re.param_re(datas['parameter']))
        print(datas['param'])
        output(datas['title'], datas['url'], datas['header'], datas['param'], datas['expected'])
        # res = self.api.api_request(datas['method'], datas['url'], datas['header'], datas['param'])
        res = requests.post(datas['url'], headers=datas['header'], data=datas['param'])
        self.log.info("the actual result :{0}".format(res.json()))
        try:
            self.assertEqual(str(eval(datas['expected'])['code']), str(res.json()['code']))
            Result = "PASS"
        except AssertionError as e:
            Result = "FAIL"
            raise e
        finally:
            self.read_data.write_back(datas['module'], datas['id'] + 1, str(res.json()['code']), Result)
