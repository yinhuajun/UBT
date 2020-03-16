import requests
from bs4 import BeautifulSoup
import re


class RomData(object):

    def __init__(cls):
        cls.url = 'http://10.10.10.1/cgi-bin/luci'
        cls.header = {'Content-Type': 'application/x-www-form-urlencoded'}
        cls.data = {'luci_username': 'root', 'luci_password': '8'}
        cls.res = requests.post(url=cls.url, headers=cls.header, data=cls.data)
        cls.soup = BeautifulSoup(cls.res.text, 'lxml')

    def getdata(self, name):
        name = self.soup.find("div", text=re.compile(name))
        brothername = name.next_sibling
        brothertext = brothername.get_text().strip()
        return brothertext
