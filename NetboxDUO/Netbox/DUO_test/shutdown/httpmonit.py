import requests
import time
import datetime
import os

# 项目路径
DatasPath = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

# 存储 sn 列表的文件
snFilePath = os.path.join(DatasPath, 'shutdown/snlist.txt')

# 装载存储时间的文档
timeFilePath = os.path.join(DatasPath, 'shutdown/basetime.txt')

# 存储结果文件
resFilePath = os.path.join(DatasPath, 'shutdown/res.txt')

# 开始查询时间  格式化为 "%Y-%m-%d %H:%M:%S"
startDateTimeStr = "2019-08-12 09:00:00"

# 结束查询时间 格式化为 "%Y-%m-%d %H:%M:%S"
endDateTimeStr = "2019-08-13 08:35:59"

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


resultFile = open(resFilePath, "w+")
resultFile.write("SN|标准结果时间|上报情况|服务端接收时间 \n")

snList = get_sn_list()

totalRes = []
totalBaseTime = 0
totalsCount = 0
totalsnoneCount = 0
totalsremaincount = 0
errorDist = {}

for sn in snList:
    resultFile.write("SN:" + sn + "======================================================\n")
    httpres = get_http_data(sn)
    dList = httpres["data"]
    targetDist = list_cover_dist(dList)

    snonecount = 0
    sremaincount = 0
    scount = str(len(targetDist))
    # 处理标准数据 和 目标数据
    for baseTime in timeRangeList:

        baseTime = baseTime.strftime("%Y-%m-%d %H:%M")
        if baseTime in targetDist:  # 正好相等
            resultFile.write(sn + "|" + baseTime + "|" + baseTime+"|"+targetDist[baseTime] + "|" + ("" if equalmins(baseTime, targetDist[baseTime]) else "时间不一致") + "\n")
            del targetDist[baseTime]
        elif offset_mins(baseTime, 1000 * 60) in targetDist:  # 真实时间 +1分钟
            resultFile.write(sn + "|" + baseTime + "|" + offset_mins(baseTime, 1000 * 60) + "|" + targetDist[offset_mins(baseTime, 1000 * 60)] + "|" + ("" if equalmins(offset_mins(baseTime, 1000 * 60), targetDist[offset_mins(baseTime, 1000 * 60)]) else "时间不一致" ) + "|偏移 +1 分钟\n")
            del targetDist[offset_mins(baseTime, 1000 * 60)]
        elif offset_mins(baseTime, -1000 * 60) in targetDist:  # 真实时间 -1分钟
            resultFile.write(sn + "|" + baseTime + "|" + offset_mins(baseTime, -1000 * 60) + "|" + targetDist[offset_mins(baseTime, -1000 * 60)] + "|" + ("" if equalmins(offset_mins(baseTime, -1000 * 60), targetDist[offset_mins(baseTime, -1000 * 60)]) else "时间不一致") + "|偏移 -1 分钟\n")
            del targetDist[offset_mins(baseTime, -1000 * 60)]
        else:
            resultFile.write(sn + "|" + baseTime + "|服务端未上报此时间的数据\n")
            snonecount = snonecount+1
            if "漏报"+baseTime in errorDist:
                errorDist["漏报"+baseTime] += 1
            else:
                errorDist["漏报"+baseTime] = 1

    # 处理目标多余的数据

    remainList = list(targetDist.keys())
    remainList.sort()

    for rtl in remainList:
        resultFile.write(sn + "|我是服务端多上报的数据|" + rtl + "|" + targetDist[rtl] + "|" + ("" if equalmins(rtl, targetDist[rtl]) else "时间不一致") + "\n")
        sremaincount = sremaincount + 1
        if "多报"+targetDist[rtl] in errorDist:
            errorDist["多报"+targetDist[rtl]] += 1
        else:
            errorDist["多报" + targetDist[rtl]] = 1
    print("sn:"+sn+" 处理完毕")
    totalRes.append(sn+"|"+str(len(baseTimeList))+"|"+scount+"|"+str(snonecount)+"|"+str(sremaincount)+"\n")
    totalBaseTime += len(baseTimeList)
    totalsCount += int(scount)
    totalsnoneCount += snonecount
    totalsremaincount += sremaincount

resultFile.write("======================总计信息================================\n")
resultFile.write("SN|标准时间个数|服务端数据个数|服务端未上报的|服务端多的个数\n")
for rtl in totalRes:
    resultFile.write(rtl)

resultFile.write("总计:"+str(totalBaseTime)+"|"+str(totalsCount)+"|"+str(totalsnoneCount)+"|"+str(totalsremaincount)+"\n")
resultFile.write("漏报率："+str(totalsnoneCount/totalBaseTime*100)+"%\n") if totalBaseTime != 0 else resultFile.write()
resultFile.write("查询时间从:"+startDateTimeStr+" - "+endDateTimeStr+"  跨度时间为  "+str((endDateTime - startDateTime))+"\n")

for key, value in errorDist.items():
    resultFile.write(key +"==" + str(value) + "\n")

resultFile.close()