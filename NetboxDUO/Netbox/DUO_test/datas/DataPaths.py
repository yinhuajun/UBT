import os
import time

# 项目路径
ProjectPath = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
# 日志路径
LogsPath = os.path.join(ProjectPath,  'los\datas{0}'.format(time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime())))
# print(LogsPath)
# 测试数据路径
DatasPath = os.path.join(ProjectPath, 'datas/Production_inspection.xlsx')
# DatasPath2 = os.path.join(ProjectPath, 'datas/writerom.xlsx')