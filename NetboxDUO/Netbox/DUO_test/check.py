# -*- coding:utf-8 -*-
import time
from selenium import webdriver
import re
from Netbox.DUO_test.ip.getip import get_ip
from Netbox.DUO_test.ssh.sshconnect import commend
from Netbox.DUO_test.ssh.sshconnect import close

P = get_ip('ipconfig')

# option = webdriver.ChromeOptions()
# option.add_argument('headless')
# driver = webdriver.Chrome(chrome_options=option)
driver = webdriver.Chrome()
waitxpath = driver.implicitly_wait(40)  # 设置隐式时间等待
xpath = driver.find_element_by_xpath


def prired(*text):
    text = str(text)
    ll = '\033[1;31;46m' + text + '\033[0m'
    print(ll)


while P:
    for i in range(1000):
        try:
            driver.get("http://10.10.10.1/cgi-bin/luci")
            Username = driver.find_element_by_xpath("//*[@id='maincontent']/form/div[1]/div[2]/div/div[1]/div/input")
            Username.clear()
            Username.send_keys("root")
            Password = xpath("//*[@id='maincontent']/form/div[1]/div[2]/div/div[2]/div/input")
            Password.clear()
            Password.send_keys("ubt3018")
            xpath("//*[@id='maincontent']/form/div[2]/input[1]").click()
            # 打印SN
            SN = xpath('/html/body/header/div/div/a').text
            print(SN)
            # 查看GPS
            GPS = xpath('//*[@id="maincontent"]/div[1]/div/div[9]/div[2]').text
            if re.match(r'^1(.*)2019', GPS):
                print(SN, 'GPS正常', GPS)
            else:
                prired(SN + 'GPS错误-------------------------' + GPS)
                time.sleep(1)
            # 查看SIM卡
            SIM = xpath('//*[@id="maincontent"]/div[1]/div/div[11]/div[2]').text
            print(SIM)
            for i in range(3):
                if re.match(r'(.*)READY$', SIM):
                    print(SN, 'SIM卡正常', SIM)
                    break
                else:
                    time.sleep(2)
                    driver.refresh()
                    prired(SN, "SIM卡错误", SIM)
                    SIM = xpath('//*[@id="maincontent"]/div[1]/div/div[11]/div[2]').text

            # 检查RTC时钟
            for i in range(10):
                try:
                    RTC = commend('cat /tmp/time')
                    break
                except:
                    print("尝试连接ssh")
                    close()
                    time.sleep(2)

            if re.match(r'^2019(.*)', RTC):
                print(SN, 'RTC正确', RTC)
            else:
                prired(SN, 'RTC错误:', RTC)
            # 检查SD卡
            SD = xpath('//*[@id="maincontent"]/div[1]/div/div[12]/div[2]').text
            if re.search(r'1|2|3|4', SD):
                print(SN, 'SD卡正确识别,脚本版本号：', SD)
            else:
                prired(SN, 'SD卡错误------------------')
            # 检查模块复位
            result = commend('lsusb')
            t = (result[28:32])
            if t == '0061':
                print(SN, '模块识别正常')
                commend('echo 10 > /tmp/lterest')
                result2 = commend('lsusb')
                time.sleep(2)
                t2 = (result2[28:32])
                if t2 != '0061':
                    print(SN, '模块复位成功')
                else:
                    prired(SN, '复位失败------------------')
            else:
                prired(SN, '模块不识别')

            commend('echo 11 > /tmp/lterest')
            close()
            # time.sleep(20)
            print('输入回车进行下一个')
            name = input()
        except:
            time.sleep(1)
            driver.refresh()
            driver.get("http://10.10.10.1/cgi-bin/luci")
        # except AssertionError as e:
        #     raise e
        # finally:
        #     time.sleep(1)
