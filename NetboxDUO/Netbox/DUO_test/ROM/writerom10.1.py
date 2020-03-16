# -*- coding:utf-8 -*-
import subprocess
import time
from selenium import webdriver
from playsound import playsound
import re


def search(pattern,text,flag):
    m=re.search(pattern,text)
    if m is not None:
          return m.group(flag)

def get_ip(cmd):
    ip_cur = '0.0.0.0'
    while ip_cur == '0.0.0.0':
        obj = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        obj.wait()
        lines = obj.stdout.readlines()
        for eachline in lines:
            eachline= eachline.decode('gbk')
            strs='IPv4 地址'
            if strs in eachline:
                content=search('IPv4 地址 . . . . . . . . . . . . :(.*?)\r\n',eachline,1)
                ip_cur = str(content)
                break
    return ip_cur
P=get_ip('ipconfig')
driver = webdriver.Chrome()
waitxpath = driver.implicitly_wait(40)  # 设置隐式时间等待
xpath=driver.find_element_by_xpath
while P:
    for i in range(1000):
        try:
            driver.get("http://192.168.10.1/cgi-bin/luci")
            Username = driver.find_element_by_xpath("//*[@id='maincontent']/form/div[1]/div[2]/div/div[1]/div/input")
            waitxpath
            Username.clear()
            Username.send_keys("root")
            Password = driver.find_element_by_xpath("//*[@id='maincontent']/form/div[1]/div[2]/div/div[2]/div/input")
            Password.clear()
            Password.send_keys("1")
            driver.find_element_by_xpath("//*[@id='maincontent']/form/div[2]/input[1]").click()
            waitxpath
            driver.find_element_by_xpath("/html/body/header/div/div/ul/li[2]/a").click()
            driver.find_element_by_xpath("/html/body/header/div/div/ul/li[2]/ul/li[8]/a").click()
            xpath('//*[@id="keep"]').click()
            xpath('//*[@id="image"]').send_keys(r'C:\Users\Administrator.PC-201805262137\Desktop\涛\2.0.4-single.bin')
            xpath('//*[@id="maincontent"]/div[2]/form/div[2]/div[2]/div/input[2]').click()
            waitxpath
            MD5 = xpath('//*[@id="maincontent"]/fieldset/ul/li[1]/code[1]').text
            if MD5 != '704e6b7f135947713f12610bde6684ab':
                break
            xpath('//*[@id="maincontent"]/div/form/input[5]').click()
            file = 'F:/python/Voicepackage/pass.mp3'
            playsound(file)
            time.sleep(8)
            driver.get("http://192.168.10.1/cgi-bin/luci")
            break
        except:
            time.sleep(1)
            driver.refresh()
            driver.get("http://192.168.10.1/cgi-bin/luci")

