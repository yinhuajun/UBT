import requests
import time
import datetime
import os
import xlwt

# 项目路径
DatasPath = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

# 存储 sn 列表的文件
snFilePath = os.path.join(DatasPath, 'shutdown/snlist.txt')

# 装载存储时间的文档
timeFilePath = os.path.join(DatasPath, 'shutdown/basetime.txt')

# 存储结果文件
resFilePath = os.path.join(DatasPath, 'shutdown/res.txt')
#初始化一个excel并指定字符集为UTF-8的
excel = xlwt.Workbook(encoding = 'utf-8')
#新建一个sheet 命名为xlwt_sheet1
sheet = excel.add_sheet('查询结果')
#设置样式
style = xlwt.XFStyle()
# 设置背景颜色
style.pattern = xlwt.Pattern()
# 设置背景颜色的模式
style.pattern.pattern = xlwt.Pattern.SOLID_PATTERN
# 背景颜色
style.pattern.pattern_fore_colour = 6



# 开始查询时间  格式化为 "%Y-%m-%d %H:%M:%S"
startDateTimeStr = "2019-08-16 00:20:00"

# 结束查询时间 格式化为 "%Y-%m-%d %H:%M:%S"
endDateTimeStr = "2019-08-16 10:59:59"

# 装载标准时间txt
timeFile = open(timeFilePath, "r")
baseTimeList = timeFile.read().splitlines()
timeFile.close()

startDateTime = time.strptime(startDateTimeStr, "%Y-%m-%d %H:%M:%S")
endDateTime = time.strptime(endDateTimeStr, "%Y-%m-%d %H:%M:%S")
startDateTime = datetime.datetime(startDateTime[0], startDateTime[1], startDateTime[2], startDateTime[3], startDateTime[4], startDateTime[5])
endDateTime = datetime.datetime(endDateTime[0], endDateTime[1], endDateTime[2], endDateTime[3], endDateTime[4], endDateTime[5])
days = (endDateTime - startDateTime).days

timeRangeList = []
daysc = 0
# 从开始时间装载天数
while days >= 0:
    for baseTime in baseTimeList:
        baseTimeD = time.strptime(baseTime, "%H:%M")
        baseTimeD = datetime.datetime(startDateTime.year, startDateTime.month, int(startDateTime.day + daysc), baseTimeD[3], baseTimeD[4], baseTimeD[5])
        if baseTimeD.timestamp() > startDateTime.timestamp() and baseTimeD.timestamp() < endDateTime.timestamp():
            timeRangeList.append(baseTimeD)
    daysc += 1
    days -= 1

# 把字符串转成时间戳毫秒形式
def string_totimestamp(st):
    return int(round(time.mktime(time.strptime(st, "%Y-%m-%d %H:%M:%S")) * 1000))


# 把时间戳毫秒转换为 精确到分钟的字符串
def timestamp_to_strm(timeStamp):
    return datetime.datetime.fromtimestamp(timeStamp / 1000).strftime("%Y-%m-%d %H:%M")


# 把字符串转成时间戳毫秒形式
def offset_mins(st, ss):
    stamp = int(round(time.mktime(time.strptime(st, "%Y-%m-%d %H:%M")) * 1000))
    return timestamp_to_strm(stamp + ss)


# 读取txt 中SN 的列表
def get_sn_list():
    snFile = open(snFilePath, "r")
    lines = snFile.read().splitlines()
    snFile.close()
    return lines


# 读取网络接口中的数据 并返回 jason  参数：sn
def get_http_data(sn):
    payload = {'sn': sn, 'start_time': string_totimestamp(startDateTimeStr), 'end_time': string_totimestamp(endDateTimeStr)}
    r = requests.get("http://device.platform.ubt.io/netboxduo/msg/get/shutdown_info", params=payload)
    return r.json()

# 读取网络接口中的数据 并返回 jason  参数：sn
def get_http_data_onoff(sn):
    payload = {'sn': sn, 'start_time': string_totimestamp(startDateTimeStr), 'end_time': string_totimestamp(endDateTimeStr)}
    r = requests.get("http://device.platform.ubt.io/netboxduo/msg/get/power_status", params=payload)
    return r.json()

# 读取dongle status 数据 并返回 jason  参数：sn
def get_http_data_status(sn):
    payload = {'sn': sn, 'start_time': string_totimestamp(startDateTimeStr), 'end_time': string_totimestamp(endDateTimeStr)}
    r = requests.get("http://device.platform.ubt.io/netboxduo/msg/get/dongle_status", params=payload)
    return r.json()



# 根据返回的结果转换为 dist
def list_cover_dist(dList):

    resDict = {}
    resDicttamp = {}
    for sdData in dList:
        if timestamp_to_strm(sdData["time"]) in resDict:

            if resDicttamp[timestamp_to_strm(sdData["time"])] > int(sdData["createTime"]):
                resDict[timestamp_to_strm(sdData["time"])] = timestamp_to_strm(sdData["createTime"])
                resDicttamp[timestamp_to_strm(sdData["time"])] = int(sdData["createTime"])
        else:
            resDict[timestamp_to_strm(sdData["time"])] = timestamp_to_strm(sdData["createTime"])
            resDicttamp[timestamp_to_strm(sdData["time"])] = int(sdData["createTime"])
    return resDict

# 根据返回的结果转换为 dist
def list_cover_dist_onoff(dList):

    resDict = {}
    resDicttamp = {}
    for sdData in dList:
        if (timestamp_to_strm(sdData["time"]) in resDict) and sdData["powerOn"] == False:

            if resDicttamp[timestamp_to_strm(sdData["time"])] > int(sdData["createTime"]):
                resDict[timestamp_to_strm(sdData["time"])] = timestamp_to_strm(sdData["createTime"])
                resDicttamp[timestamp_to_strm(sdData["time"])] = int(sdData["createTime"])
        elif sdData["powerOn"] == False:
            resDict[timestamp_to_strm(sdData["time"])] = timestamp_to_strm(sdData["createTime"])
            resDicttamp[timestamp_to_strm(sdData["time"])] = int(sdData["createTime"])
    return resDict


# 判断两个字符串分钟数是否相等 左右浮动 1分钟
def equalmins(sm,tm):
    if sm == tm:
        return True
    elif sm == offset_mins(tm, 1000 * 60):
        return True
    elif sm == offset_mins(tm, -1000 * 60):
        return True
    else:
        return False

etitle = ['SN','标准结果时间', '上报时间', '服务端接收时间', '备注','正健开关机是否存在关机','dongle status是否存在']

snList = get_sn_list()

totalRes = []
totalBaseTime = 0
totalsCount = 0
totalsnoneCount = 0
totalsremaincount = 0
errorDist = {}

for sn in snList:

    print("开始处理 SN:"+sn)
    httpres = get_http_data(sn)

    dList = httpres["data"]
    targetDist = list_cover_dist(dList)

    httpres_onoff = get_http_data_onoff(sn)
    targetDist_onoff = list_cover_dist_onoff(httpres_onoff["data"])

    httpres_status = get_http_data_status(sn)
    targetDist_status = list_cover_dist(httpres_status["data"])

    snonecount = 0
    sremaincount = 0
    scount = str(len(targetDist))

    #写标题
    for it in etitle:
        sheet.write(0, etitle.index(it)+snList.index(sn)*len(etitle), it)

        # 处理标准数据 和 目标数据
    for baseTime in timeRangeList:
        baseTimeIdx = timeRangeList.index(baseTime)+1
        baseTime = baseTime.strftime("%Y-%m-%d %H:%M")

        #开始处理
        if baseTime in targetDist:  # 正好相等

            sheet.write(baseTimeIdx, 0 + snList.index(sn) * len(etitle), sn)
            sheet.write(baseTimeIdx, 1 + snList.index(sn) * len(etitle), baseTime)
            sheet.write(baseTimeIdx, 2 + snList.index(sn) * len(etitle), baseTime)
            sheet.write(baseTimeIdx, 3 + snList.index(sn) * len(etitle), targetDist[baseTime])
            sheet.write(baseTimeIdx, 4 + snList.index(sn) * len(etitle), "" if equalmins(baseTime, targetDist[baseTime]) else "时间不一致")
            del targetDist[baseTime]
        elif offset_mins(baseTime, 1000 * 60) in targetDist:  # 真实时间 +1分钟

            sheet.write(baseTimeIdx, 0 + snList.index(sn) * len(etitle), sn)
            sheet.write(baseTimeIdx, 1 + snList.index(sn) * len(etitle), baseTime)
            sheet.write(baseTimeIdx, 2 + snList.index(sn) * len(etitle), offset_mins(baseTime, 1000 * 60))
            sheet.write(baseTimeIdx, 3 + snList.index(sn) * len(etitle), offset_mins(baseTime, 1000 * 60))
            sheet.write(baseTimeIdx, 4 + snList.index(sn) * len(etitle),
                        "" if equalmins(offset_mins(baseTime, 1000 * 60), targetDist[offset_mins(baseTime, 1000 * 60)]) else "时间不一致|"+"|偏移 +1 分钟")
            del targetDist[offset_mins(baseTime, 1000 * 60)]

        elif offset_mins(baseTime, -1000 * 60) in targetDist:  # 真实时间 -1分钟

            sheet.write(baseTimeIdx, 0 + snList.index(sn) * len(etitle), sn)
            sheet.write(baseTimeIdx, 1 + snList.index(sn) * len(etitle), baseTime)
            sheet.write(baseTimeIdx, 2 + snList.index(sn) * len(etitle), offset_mins(baseTime, -1000 * 60))
            sheet.write(baseTimeIdx, 3 + snList.index(sn) * len(etitle), offset_mins(baseTime, -1000 * 60))
            sheet.write(baseTimeIdx, 4 + snList.index(sn) * len(etitle),
                        "" if equalmins(offset_mins(baseTime, -1000 * 60), targetDist[offset_mins(baseTime, -1000 * 60)]) else "时间不一致" + "|偏移 -1 分钟")
            del targetDist[offset_mins(baseTime, 1000 * 60)]
        else:

            sheet.write(baseTimeIdx, 0 + snList.index(sn) * len(etitle), sn, style)
            sheet.write(baseTimeIdx, 1 + snList.index(sn) * len(etitle), baseTime, style)
            sheet.write(baseTimeIdx, 2 + snList.index(sn) * len(etitle), "", style)
            sheet.write(baseTimeIdx, 3 + snList.index(sn) * len(etitle), "", style)
            sheet.write(baseTimeIdx, 4 + snList.index(sn) * len(etitle), "服务端未上报此时间的数据", style)

            if offset_mins(baseTime, 1000 * 60) in targetDist_onoff:
                sheet.write(baseTimeIdx, 5 + snList.index(sn) * len(etitle), "正健上报的有 "+targetDist_onoff[offset_mins(baseTime, 1000 * 60)], style)
            elif offset_mins(baseTime, -1000 * 60) in targetDist_onoff:
                sheet.write(baseTimeIdx, 5 + snList.index(sn) * len(etitle),
                            "正健上报的有 " + targetDist_onoff[offset_mins(baseTime, -1000 * 60)], style)
            elif offset_mins(baseTime, 2000 * 60) in targetDist_onoff:
                sheet.write(baseTimeIdx, 5 + snList.index(sn) * len(etitle), "正健上报的有 "+targetDist_onoff[offset_mins(baseTime, 2000 * 60)], style)
            elif offset_mins(baseTime, -2000 * 60) in targetDist_onoff:
                sheet.write(baseTimeIdx, 5 + snList.index(sn) * len(etitle),
                            "正健上报的有 " + targetDist_onoff[offset_mins(baseTime, -2000 * 60)], style)
            elif baseTime in targetDist_onoff:
                sheet.write(baseTimeIdx, 5 + snList.index(sn) * len(etitle), "正健上报的有 "+targetDist_onoff[baseTime], style)

            if offset_mins(baseTime, 1000 * 60) in targetDist_status:
                sheet.write(baseTimeIdx, 6 + snList.index(sn) * len(etitle), "正健上报的有 "+targetDist_status[offset_mins(baseTime, 1000 * 60)], style)
            elif offset_mins(baseTime, -1000 * 60) in targetDist_status:
                sheet.write(baseTimeIdx, 6 + snList.index(sn) * len(etitle),
                            "正健上报的有 " + targetDist_status[offset_mins(baseTime, -1000 * 60)], style)
            elif offset_mins(baseTime, 2000 * 60) in targetDist_status:
                sheet.write(baseTimeIdx, 6 + snList.index(sn) * len(etitle), "正健上报的有 "+targetDist_status[offset_mins(baseTime, 2000 * 60)], style)
            elif offset_mins(baseTime, -2000 * 60) in targetDist_status:
                sheet.write(baseTimeIdx, 6 + snList.index(sn) * len(etitle),
                            "正健上报的有 " + targetDist_status[offset_mins(baseTime, -2000 * 60)], style)
            elif baseTime in targetDist_status:
                sheet.write(baseTimeIdx, 6 + snList.index(sn) * len(etitle), "正健上报的有 "+targetDist_status[baseTime], style)
            snonecount += 1
            if "漏报"+baseTime in errorDist:
                errorDist["漏报"+baseTime] += 1
            else:
                errorDist["漏报"+baseTime] = 1
    sheet.write(len(timeRangeList) + 1, 0 + snList.index(sn) * len(etitle), "漏报总计：")
    sheet.write(len(timeRangeList) + 1, 1 + snList.index(sn) * len(etitle), snonecount)


excel.save(os.path.join(DatasPath, 'shutdown/result.xls'))

