from pywifi import const, PyWiFi, Profile
import time
import re
import time
from selenium import webdriver
import subprocess
from Netbox.DUO_test.ip.getip import get_ip


# wifi类

class wifi(object):
    def __init__(self):
        self.wifi = PyWiFi()  # 创建一个无线对象
        self.interfaces = self.wifi.interfaces()  # 获取无线网卡接口
        self.iface = self.interfaces[-1]  # 获取第一个无线网卡接口
        # self.iface1 = self.interfaces[-1]

    # 获取无线网卡接口
    def get_wifi_interfaces(self):
        num = len(self.interfaces)
        if num <= 0:
            print(u'未找到无线网卡接口!')
            exit()
        if num == 1:
            print(u'无线网卡接口: %s' % (self.iface.name()))
            return self.iface
        else:
            print('%-4s   %s\n' % (u'序号', u'网卡接口名称'))
            for i, w in enumerate(self.interfaces):
                print('%-4s   %s' % (i, w.name()))
            while True:
                # iface_no = input('请选择网卡接口序号：')
                iface_no = 1
                # iface_no = input('请选择网卡接口序号：'.decode('utf-8').encode('gbk'))1
                no = int(iface_no)
                if no >= 0 and no < num:
                    return self.interfaces[no]

    # 查看无线网卡是否处于连接状态
    def check_interfaces(self):
        if self.iface.status() in [const.IFACE_CONNECTED, const.IFACE_CONNECTING]:
            print('无线网卡：%s 已连接。' % self.iface.name())
            return True
        else:
            print('无线网卡：%s 未连接。' % self.iface.name())
            return False

    # 扫描周围wifi
    def scan_wifi(self):
        self.iface.scan()  # 扫描周围wifi
        time.sleep(1)  # 不缓冲显示不出来
        result = self.iface.scan_results()  # 获取扫描结果，wifi可能会有重复
        has = []  # 初始化已扫描到的wifi
        wifi_list = []  # 初始化扫描结果
        for i in result:
            if i not in has:  # 若has中没有该wifi，则
                has.append(i)  # 添加到has列表
                if i.signal > -90:  # 信号强度<-90的wifi几乎连不上
                    DUOwifi = re.match(r'^(BusMovie\.net_)(\d{4}$)', i.ssid)
                    if DUOwifi:
                        Sn = DUOwifi[2]
                        DUOSN = 'ND301802011{0}'.format(Sn)
                        wifi_list.append((i.ssid, i.signal, DUOSN))  # 添加到wifi列表
                        print('名称：{0}，wifi信号强度：{1}，SN：ND301802011{2}'.format(i.ssid, i.signal, Sn))  # 输出wifi名称
        # return sorted(wifi_list, key=lambda x: x[1], reverse=True)  # 按信号强度由高到低排序

        return sorted(wifi_list, key=lambda x: x[2])  # 按SNc从小到大排序

    # 连接wifi
    def connect_wifi(self, wifi_name):
        self.iface.disconnect()  # 断开无线网卡连接
        time.sleep(1)  # 缓冲1秒
        profile_info = Profile()  # wifi配置文件
        profile_info.ssid = wifi_name  # wifi名称
        # profile_info.auth = const.AUTH_ALG_OPEN  # 需要密码
        profile_info.akm.append(const.AKM_TYPE_NONE)  # 加密类型
        profile_info.cipher = const.CIPHER_TYPE_NONE  # 加密单元
        # profile_info.key = wifi_password  # wifi密码
        self.iface.remove_all_network_profiles()  # 删除其他配置文件
        tmp_profile = self.iface.add_network_profile(profile_info)  # 加载配置文件
        self.iface.connect(tmp_profile)  # 连接
        # 尝试5秒是否能成功连接(时间过短可能会导致正确密码尚未连接成功)
        time.sleep(5)
        if self.iface.status() == const.IFACE_CONNECTED:
            print('==========================================================================')
            print('wifi：{0} 连接成功'.format(wifi_name), end='\n')
            print('==========================================================================')
            return True
        else:
            print('wifi：{0}连接失败'.format(wifi_name), end='')
            return False

    # 断开无线网卡已连接状态
    def disconnect_wifi(self):
        self.iface.disconnect()
        if self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]:
            print('无线网卡：%s 已断开。' % self.iface.name())
        else:
            print('无线网卡：%s 未断开。' % self.iface.name())

    def prired(self, *text):
        text = str(text)
        ll = '\033[1;31;46m' + text + '\033[0m'
        print(ll)

    # @classmethod
    # def scanning(self):
    #     # wifi = wifi()  # 实例化wifi类
    #     wifi().get_wifi_interfaces()  # 获取网卡接口
    #     wifi().check_interfaces()  # 检测网卡连接状态
    #     print('正在扫描可见NetBox DUO...')
    #     wifiList = wifi().scan_wifi()  # 扫描周围wifi
    #     return wifiList


if __name__ == '__main__':
    wifi = wifi()  # 实例化wifi类
    wifi.get_wifi_interfaces()  # 获取网卡接口
    wifi.check_interfaces()  # 检测网卡连接状态
    print('正在扫描可见NetBox DUO...')
    wifiList = wifi.scan_wifi()  # 扫描周围wifi
    if not wifiList:
        print("未扫描到NetBox DUO WIFI...")

    # 连接wifi
    for i in wifiList:
        print('正在连接%s，请耐心等待...' % i[0])
        start = time.time()
        try:
            result = wifi.connect_wifi(i[0])  # 尝试连接wifi
            if result == True:  # 若找连接成功，继续操作
                print("连接成功")
        except:
            continue
