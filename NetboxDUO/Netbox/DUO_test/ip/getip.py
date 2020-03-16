# -*- coding:utf-8 -*-
import subprocess
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