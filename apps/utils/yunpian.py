#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
# time:'2018/3/27 22:44:50下午'

import requests,json


class YunPian():
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        parmas = {
            'apikey':self.api_key,
            'mobile':mobile,
            "text":"【xxx】您的验证码是{}。如非本人操作，请忽略本短信".format(code),

        }
        response = requests.post(self.single_send_url,data=parmas)
        re_dict = json.loads(response.text)
        return re_dict

if __name__ == '__main__':
    yun_pian = YunPian('e5easd3dadsadsdsadasaa1cddsad0ed8472e')
    yun_pian.send_sms('2017','18312743371')