# yinhuajun19.7.17
from Netbox.DUO_test.datas.read_datas import ReadDatas
from Netbox.DUO_test.datas import DataPaths
from Netbox.DUO_test.WIFI.wifi import wifi
from Netbox.DUO_test.ROM.getRomData import RomData
from Netbox.DUO_test.datas.MyLog import MyLogs
import time
import sys
from ddt import ddt, data
import unittest
from Netbox.DUO_test.ssh.sshconnect import commend

sheet = "sheet1"
testdata = ReadDatas(DataPaths.DatasPath).read_datas(sheet)
wifi = wifi()  # 实例化wifi类
log = MyLogs()


@ddt
class RunCheck(unittest.TestCase):
    wifi.get_wifi_interfaces()  # 获取网卡接口
    wifi.check_interfaces()  # 检测网卡连接状态
    print('正在扫描可见NetBox DUO...')
    wifiList = wifi.scan_wifi()  # 扫描周围wifi

    @classmethod
    def setUpClass(cls):
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        wifiSN = cls.wifiList
        if not wifiSN:
            print("未扫描到WIFI......")
            sys.exit(0)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    # 连接wifi
    @data(*testdata)
    def test_writeExcel(self, dates):
        wifiSN = self.wifiList
        for i in range(len(wifiSN)):
            if str(dates['SN'])[-8:] == str(wifiSN[i][2])[-8:] and dates['WIFI'] is None:
                try:
                    wifi.connect_wifi(wifiSN[i][0])
                    wifiname = wifiSN[i][0]
                    intensity = wifiSN[i][1]
                    print("从后台爬取GPS，SIM卡状态，脚本版本号数据，请等待。。。。。。")
                    gps = RomData().getdata('GPS')
                    sim = RomData().getdata('SIM Status')
                    sd = RomData().getdata('Scripts Version')
                    fv = RomData().getdata('Firmware Version')
                    rtc, rst = 'Null', 'fail'

                    print("通过ssh连接获取RTC，尝试模块复位，请等待。。。。。")
                    rtc = commend('cat /tmp/time')  # 获取rtc时间
                    # 检查模块复位
                    result = commend('lsusb')
                    iden = (result[28:32])  # 取金雅拓模块标识
                    if iden == '0061':
                        commend('echo 10 > /tmp/lterest')
                        time.sleep(3)
                        result2 = commend('lsusb')
                        t2 = (result2[28:32])
                        if t2 != '0061':
                            rst = 'pass'
                            commend('echo 11 > /tmp/lterest')  # 恢复模块供电

                            # commend('sh /bin/reset_gemalto.sh')  # 调用脚本重启，检查之后是否识别
                            # commend('echo 11 > /tmp/lterest')
                            # # time.sleep(20)
                            # result3 = commend('lsusb')
                            # t3 = (result3[28:32])
                            # if t3 == '0061':
                            #     rst = 'pass'
                            # else:
                            #     print('复位失败------------------')
                            #     rst = 'fail'
                        else:
                            print('模块断电失败------------------')
                            rst = 'fail'
                    else:
                        print('模块不识别')
                        iden = 'fail'
                    # time.sleep(5)
                    # commend('echo 11 > /tmp/lterest')  # 恢复模块供电
                    try:
                        self.read_data.write_back(sheet, dates['id'] + 1, wifiname, intensity, gps, rtc, sim, fv, sd,
                                                  iden,
                                                  rst)  # 将结果写到文件中
                        print(wifiSN[i][2] + "测试完成，结果写入excel中")
                    except:
                        print("文件写入错误")
                except AssertionError as e:
                    raise e


if __name__ == '__main__':
    unittest.main()
    # RC = RunCheck()
    # RC.writeExcel()
