import subprocess
import re
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from playsound import playsound


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
            driver.get("http://192.168.1.1/cgi-bin/luci")
            Username = driver.find_element_by_xpath("//*[@id='maincontent']/form/div[1]/fieldset/fieldset/div[1]/div/input")
            waitxpath
            Username.clear()
            Username.send_keys("root")
            Password = driver.find_element_by_xpath('//*[@id="focus_password"]')
            Password.clear()
            Password.send_keys("a")
            driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[2]/input[1]').click()
            waitxpath
            attrible = xpath('/html/body/header/div/div/ul/li[2]/a')
            ActionChains(driver).move_to_element(attrible).perform()
            xpath("/html/body/header/div/div/ul/li[2]/ul/li[8]/a").click()
            xpath('//*[@id="keep"]').click()
            xpath('//*[@id="image"]').send_keys(
                r'C:\Users\Administrator.PC-201805262137\Desktop\涛\2.0.3-single.bin')
            xpath('//*[@id="maincontent"]/fieldset/fieldset[2]/form/div[2]/div[2]/div/input[2]').click()
            waitxpath
            MD5 = xpath('//*[@id="maincontent"]/fieldset/ul/li[1]/code').text
            if MD5 != '301cd1d8ea0ef9ac8cd41d781e6240a6':
                break
            xpath('//*[@id="maincontent"]/div/form[2]/input[3]').click()
            file = 'F:/python/Voicepackage/pass.mp3'
            playsound(file)
            time.sleep(7)
            driver.refresh()
            break
        except:
            driver.refresh()



