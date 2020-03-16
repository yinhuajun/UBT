# -*- coding:utf-8 -*-
from aip import AipSpeech  # baidu-aip
from playsound import playsound

""" 你的 APPID AK SK """
APP_ID = '16193567'
API_KEY = 'rT9DZ9XbtKqD6FHrlzPzdsQq'
SECRET_KEY = 'empVFCmGYZRlDkrwGEZe8LrLaRLvPi59'


class yuyin():
    def du(self, text):
        self.text = text
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        result = client.synthesis(text, 'zh', 1, {
            'vol': 5, 'per': 1
        })
        file = "F:/python/Voicepackage/" + text + ".mp3"
        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            with open(file, 'wb') as f:
                f.write(result)
        playsound(file)
if __name__ == '__main__':
    p=yuyin()
    p.du('lei')
