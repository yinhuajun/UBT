# -*- coding:utf-8 -*-
# @Author   :yin
# @File     :getReturnValue.py
# @software :PyCharm



def getReturnValue(Responses,attribute):
    if Responses.get(attribute):
        return Responses[attribute]
    else:
        for Object in Responses:
            if isinstance(Responses[Object],list):
                Responses[Object] = Responses[Object][0]
            if isinstance(Responses[Object],dict):
                if attribute in Responses[Object]:
                    return Responses[Object][attribute]