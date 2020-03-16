import os
import re
import sys
import time
import xlwt
import datetime

#  ============= 变量值，可以被变更的值

# 时间相关,查询当前时间多长之前的 秒
import requests

timeRange = 1 * 3600

# 文件名相关
snFileName = 'sn.txt'  # sn列表来源的路径

# 服务端访问路径
# 测试环境
serverBaseUrl = ''
# 正式环境
#serverBaseUrl = ''

# ============== 变量值结束
# 常量值

# 时间范围时间戳
startTimeTamp = str(int((time.time() - timeRange) * 1000))
endTimeTamp = str(int(time.time() * 1000))

# 文件夹路径
fileDir = os.path.split(os.path.realpath(__file__))[0]
snFilePath = fileDir + '/' + snFileName
snList = []
snNotMatchStr = ''

# 初始化一个excel并指定字符集为UTF-8的
writeExcel = xlwt.Workbook(encoding='utf-8')
# 新建一个sheet 命名为xlwt_sheet1
writeSheet = writeExcel.add_sheet('查询结果')
startCols = 1
titleList = ["SN", "最后在线状态", "最后开关机状态-正健","延迟关机时间", "GPS信息","ROM 版本号","电源板版本号","脚本版本号","网络模块信息","6-9列更新时间","gsenser最新"]


# 把时间戳毫秒转换为 精确到分钟的字符串
def timestamp_to_strm(timeStamp):
    return datetime.datetime.fromtimestamp(timeStamp / 1000).strftime("%Y-%m-%d %H:%M:%S")


# 设置背景颜色
def setStyle(color_pa):
    pattern = xlwt.Pattern()  # Create the Pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = color_pa  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
    style = xlwt.XFStyle()  # Create the Pattern
    style.pattern = pattern  # Add Pattern to Style

    return style


# 程序开始
# step1 读取SNFile 的内容，并循环
print('###### 程序要开始运行了请睁大双眼 ######')

snFile = open(snFilePath, "r")
snLines = snFile.read().splitlines()
snFile.close()

for snLine in snLines:
    snLine = snLine.strip()

    if snLine is '':
        continue

    # 先开始拼配带有范围的
    m = re.match(r'^\[(ND301802011\d{4})-(ND301802011\d{4})\]$', snLine)
    if m:
        sSNNum = re.match(r'ND(.*)', m.group(1)).group(1)
        eSNNum = re.match(r'ND(.*)', m.group(2)).group(1)

        for snNum in range(int(sSNNum), int(eSNNum) + 1):
            if 'ND' + str(snNum) not in snList:
                snList.append('ND' + str(snNum))

    # 匹配单行 SN 规则
    ms = re.match(r'^(ND301802011\d{4})$', snLine)
    if ms:
        if snLine not in snList:
            snList.append(snLine)

    if not (ms or m):
        snNotMatchStr += ("第 " + str(snLines.index(snLine) + 1) + " 行:" + str(snLine) + "|")

print(">>>>step1: 读取SN 列表，成功装载 " + str(len(snList)) + " 个 SN " + (
    ',失败读取的SN为：' + snNotMatchStr if snNotMatchStr == '' else ''))

snList.sort()

# 开始循环获取结果
for snLine in snList:

    idx = snList.index(snLine)

    writeSheet.write(idx + 1, 0, snLine)

    sys.stdout.write('\r' + '[' + '>' * idx + ' ' * (len(snList) - idx) + ']%s%%' % int(
        (idx + 1) / len(snList) * 100) + '   当前SN：' + snLine)
    sys.stdout.flush()
    requestParams = {'sn': snLine, 'start_time': startTimeTamp, 'end_time': endTimeTamp}

    # 获取在线状态 增加的第一列
    r = requests.get(serverBaseUrl + "msg/get/online_status", params=requestParams)
    if len(r.json()['data']) > 0:
        lineRes = sorted(r.json()["data"], key=lambda e: e.__getitem__('time'), reverse=True)[0]
        writeSheet.write(idx + 1, startCols, timestamp_to_strm(lineRes["time"]) + "|" + str(lineRes["online"]))

    # 获取开关机状态，最后一条,增加的第二列
    r = requests.get(serverBaseUrl + "msg/get/power_status", params=requestParams)
    if len(r.json()['data']) > 0:
        lineRes = sorted(r.json()["data"], key=lambda e: e.__getitem__('time'), reverse=True)[0]
        writeSheet.write(idx + 1, startCols + 1, timestamp_to_strm(lineRes["time"]) + "|" + str(lineRes["powerOn"]))

    # 获取开关机状态，最后一条,增加的第3列
    r = requests.get(serverBaseUrl + "msg/get/shutdown_info", params=requestParams)
    if len(r.json()['data']) > 0:
        lineRes = sorted(r.json()["data"], key=lambda e: e.__getitem__('time'), reverse=True)[0]
        writeSheet.write(idx + 1, startCols + 2, timestamp_to_strm(lineRes["time"]))
    else:
        writeSheet.write(idx + 1, startCols + 2, '', setStyle(53))

    # 获取最新的GPS,增加的第4列
    r = requests.get(serverBaseUrl + "msg/get/gps", params=requestParams)
    if len(r.json()['data']) > 0:
        lineRes = sorted(r.json()["data"], key=lambda e: e.__getitem__('gpsTime'), reverse=True)[0]
        # 数据格式  GPS时间|纬度|经度
        writeSheet.write(idx + 1, startCols + 3,
                         timestamp_to_strm(lineRes["gpsTime"]) + "|" + str(lineRes["latitude"]) + "|" + str(
                             lineRes["longitude"]), setStyle(1) if lineRes["status"] else setStyle(53))
    else:
        writeSheet.write(idx + 1, startCols + 3, '', setStyle(53))

    # 获取最新的systemInfo ,增加的第5-9列
    r = requests.get(serverBaseUrl + "msg/get/sysinfo", params=requestParams)
    if len(r.json()['data']) > 0:
        lineRes = sorted(r.json()["data"], key=lambda e: e.__getitem__('routerTime'), reverse=True)[0]

        # 第5列 ROM 版本号
        writeSheet.write(idx + 1, startCols + 4, lineRes["duoRomVersion"])
        # 第6列 电源板版本号
        writeSheet.write(idx + 1, startCols + 5, lineRes["powerRomVersion"])
        # 第7列 脚本版本号
        writeSheet.write(idx + 1, startCols + 6, lineRes["duoAppVersion"])
        # 第8列 模块的部分信息
        if len(lineRes["interfaces"]) > 0:
            interfaceLine = lineRes["interfaces"][0]
            writeSheet.write(idx + 1, startCols + 7, interfaceLine["interfaceName"]+"|"+interfaceLine["iccid"], setStyle(1) if interfaceLine["iccid"] != '' else setStyle(53))
        # 第9列 systemInfo 更新时间
        writeSheet.write(idx + 1, startCols + 8, timestamp_to_strm(lineRes["routerTime"]))
    else:
        writeSheet.write(idx + 1, startCols + 4, '', setStyle(53))

    # 获取最新的gsennor 信息，第10列
    r = requests.get(serverBaseUrl + "msg/get/gsenser", params=requestParams)
    if len(r.json()['data']) > 0:
        lineRes = sorted(r.json()["data"], key=lambda e: e.__getitem__('time'), reverse=True)[0]
        # 数据格式

        gsennorStr = ""
        gstyle = 1
        if lineRes["posXWarning"] == 1 :
            gsennorStr += ("X 轴,值为："+str(lineRes["xmax"]))
            gstyle = 24
        if lineRes["negXWarning"] == 1 :
            gsennorStr += ("X 轴,值为："+str(lineRes["xmin"]))
            gstyle = 24
        if lineRes["posYWarning"] == 1 :
            gsennorStr += ("Y 轴,值为："+str(lineRes["ymax"]))
            gstyle = 27
        if lineRes["negYWarning"] == 1 :
            gsennorStr += ("Y 轴,值为："+str(lineRes["ymin"]))
            gstyle = 27
        if lineRes["posZWarning"] == 1 :
            gsennorStr += ("Z 轴,值为："+str(lineRes["zmax"]))
            gstyle = 46
        if lineRes["negZWarning"] == 1 :
            gsennorStr += ("Z 轴,值为："+str(lineRes["zmin"]))
            gstyle = 46

        writeSheet.write(idx + 1, startCols + 9,
                         timestamp_to_strm(lineRes["time"]) + "|" + gsennorStr,setStyle(gstyle))
    else:
        writeSheet.write(idx + 1, startCols + 9, '', setStyle(53))

# 开始写标题栏
for titleLine in titleList:
    writeSheet.write(0, titleList.index(titleLine), titleLine)
outputFileName = fileDir + '/查询设备信息_' + datetime.datetime.now().strftime('%m%d_%H%M') + '.xls'
print("\n > 正在保存 excel保存的路径为："+outputFileName)
writeExcel.save(outputFileName)
print('###### 运行结束请查看结果 ######')