# 尹华军19年7月17日
from Netbox.DUO_test.datas.read_datas import ReadDatas
from Netbox.DUO_test.datas import DataPaths
from Netbox.DUO_test.WIFI.wifi import wifi
from ddt import ddt, data
import unittest
import time
from selenium import webdriver
import sys

wifi = wifi()  # 实例化wifi类
sheet = "writerom"
testdata = ReadDatas(DataPaths.DatasPath).read_datas(sheet)
nowMD5 = '274cc8456bd6bbee777002292cbfebc2'
nowfile = r'C:\Users\Administrator.PC-201805262137\Desktop\涛\openwrt-18.06-snapshot-2.0.0-2.0.8-single.bin'


@ddt
class RunCheck(unittest.TestCase):
    wifi.get_wifi_interfaces()  # 获取网卡接口
    wifi.check_interfaces()  # 检测网卡连接状态
    print('正在扫描可见NetBox DUO...')
    wifiList = wifi.scan_wifi()  # 扫描周围wifi

    @classmethod
    def setUpClass(cls):
        cls.read_data = ReadDatas(DataPaths.DatasPath)
        cls.driver = webdriver.Chrome()
        cls.waitxpath = cls.driver.implicitly_wait(40)  # 设置隐式时间等待
        cls.xpath = cls.driver.find_element_by_xpath
        wifiSN = cls.wifiList
        if not wifiSN:
            print("未扫描到WIFI......")
            cls.driver.quit()
            sys.exit(0)

    # 连接wifi
    @data(*testdata)
    def test_writeExcel(self, dates):
        wifiSN = self.wifiList
        driver = self.driver
        xpath = self.xpath

        for i in range(len(wifiSN)):
            if str(dates['SN'])[-8:] == str(wifiSN[i][2])[-8:] and dates['result'] is None:
                try:
                    wifi.connect_wifi(wifiSN[i][0])  # l连接wifi
                    driver.get("http://10.10.10.1/cgi-bin/luci")
                    Username = driver.find_element_by_xpath(
                        "//*[@id='maincontent']/form/div[1]/div[2]/div/div[1]/div/input")
                    Username.clear()
                    Username.send_keys("root")
                    Password = driver.find_element_by_xpath(
                        "//*[@id='maincontent']/form/div[1]/div[2]/div/div[2]/div/input")
                    Password.clear()
                    Password.send_keys("")
                    driver.find_element_by_xpath("//*[@id='maincontent']/form/div[2]/input[1]").click()
                    driver.find_element_by_xpath("/html/body/header/div/div/ul/li[2]/a").click()
                    driver.find_element_by_xpath("/html/body/header/div/div/ul/li[2]/ul/li[8]/a").click()
                    xpath('//*[@id="keep"]').click()
                    xpath('//*[@id="image"]').send_keys(nowfile)
                    xpath('//*[@id="maincontent"]/div[2]/form/div[2]/div[2]/div/input[2]').click()
                    time.sleep(6)
                    MD5 = xpath('//*[@id="maincontent"]/fieldset/ul/li[1]/code[1]').text
                    if MD5 != nowMD5:
                        break
                    xpath('//*[@id="maincontent"]/div/form/input[5]').click()
                    result = 'pass'
                except AssertionError as e:
                    raise e

                try:
                    self.read_data.write_wifi(sheet, dates['id'] + 1, result)  # 将结果写到文件中
                    print(wifiSN[i][2] + "  ROM刷写完成，结果写入excel中")
                except:
                    print("文件写入错误")


if __name__ == '__main__':
    unittest.main()
