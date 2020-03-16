import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from playsound import playsound
from Netbox.DUO_test.ip import getip

nowMD5 = 'ef7332ada8379d93f707e185a0807e54'
nowfile = r'C:\Users\Administrator.PC-201805262137\Desktop\涛\openwrt-18.06-snapshot-2.0.0-2.0.7-single.bin'

P = getip.get_ip('ipconfig')
driver = webdriver.Chrome()
xpath = driver.find_element_by_xpath
while P:
    for i in range(100):
        try:
            driver.get("http://192.168.1.1/cgi-bin/luci")
            Username = xpath(
                "//*[@id='maincontent']/form/div[1]/fieldset/fieldset/div[1]/div/input")
            Username.clear()
            Username.send_keys("root")
            Password = xpath('//*[@id="focus_password"]')
            Password.clear()
            Password.send_keys("")
            xpath('//*[@id="maincontent"]/form/div[2]/input[1]').click()
            attrible = xpath('/html/body/header/div/div/ul/li[2]/a')
            ActionChains(driver).move_to_element(attrible).perform()
            xpath("/html/body/header/div/div/ul/li[2]/ul/li[8]/a").click()
            xpath('//*[@id="keep"]').click()
            xpath('//*[@id="image"]').send_keys(nowfile)
            xpath('//*[@id="maincontent"]/fieldset/fieldset[2]/form/div[2]/div[2]/div/input[2]').click()
            MD5 = xpath('//*[@id="maincontent"]/fieldset/ul/li[1]/code').text
            if MD5 != nowMD5:
                break
            xpath('//*[@id="maincontent"]/div/form[2]/input[3]').click()
            file = 'F:/python/Voicepackage/pass.mp3'
            playsound(file)
            time.sleep(7)
            driver.refresh()
            break
        except:
            driver.refresh()
