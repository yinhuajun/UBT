# -*- coding:utf-8 -*-
# @Time     :2019/4/8 13:17
# @Author   :Tester_Liang
# @Email    :649626809@qq.com
# @File     :run.py
# @software :PyCharm

from BusProject.Linebus_Platform_API import HTMLTestRunnerNew
from BusProject.Linebus_Platform_API.common import DataPaths
from BusProject.Linebus_Platform_API.common.suite_case import SuiteCase
from BusProject.Linebus_Platform_API.common.read_config import Read_Config
from BusProject.Linebus_Platform_API.common.MyLog import MyLogs

with open(DataPaths.ReportPath, 'wb+') as file:
    button = Read_Config().read_config(DataPaths.ConfigPath, 'CASE', 'switch')
    caselist = eval(Read_Config().read_config(DataPaths.ConfigPath, 'CASE', 'caselist'))
    casedir=Read_Config().read_config(DataPaths.ConfigPath, 'DIR', 'switch')
    if casedir.upper()=="ALL":
        casepath=DataPaths.CasePath
    else:
        casepath =DataPaths.CasePath+'/{0}'.format(casedir)
    suite=SuiteCase().suitecase(casepath,button,caselist)
    runner = HTMLTestRunnerNew.HTMLTestRunner(file, verbosity=2, title="Linebus_Platform_API", description="2019/5/28",
                                                  tester='Tester_yin')
    try:
        runner.run(suite)
    except Exception as e:
        MyLogs().error("执行用例失败:{0}".format(e))

