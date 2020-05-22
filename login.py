# -*- coding: utf-8 -*-
"""
Created on Fri May 22 14:57:18 2020

@author: VJ
"""

import requests
import time
import json
import hashlib
import execjs
import random
from pprint import pprint
from geetest2.geetest import crack

class Login():
    def __init__(self):
        self.session = requests.Session()
        self.referer = 'https://www.tianyancha.com/'
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'www.tianyancha.com',
            'Origin': 'https://www.tianyancha.com',
            'Pragma': 'no-cache',
            'Referer': self.referer,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.phone_number = '13761068718'
        self.password = 'jiang123'

    def get_captcha(self):
        url = 'https://www.tianyancha.com/verify/geetest.xhtml'
        payload = {
            'uuid': int(time.time() * 1000)
        }

        # post payload 请求需要加上这样的头
        self.headers['Content-Type'] = 'application/json; charset=UTF-8'

        result = self.session.post(url, data=json.dumps(payload), headers=self.headers).json()
        if result['state'] == 'ok':
            return result['data']['gt'], result['data']['challenge'], self.referer
        else:
            return None
    
    def get_validate(self):
        while True:
            data = self.get_captcha()
            if data:
                break
            time.sleep(random.random())
        result = crack(data[0], data[1], data[2])
        #print(result)
        validate = {
                    'challenge':result['challenge'],
                    'seccode':'{}|jordan'.format(result['data']['validate']),
                    'validate':result['data']['validate']
                    }
        #print(validate)
        return validate             
# =============================================================================
#     if __name__ == '__main__':
#         validate = Login()
#         validate.get_validate()
# =============================================================================
    
    def encrypt_passwd(self):
        '''
            将明文密码转化为密文密码，以后密码加密先去MD5那里看看先
        '''
        md5 = hashlib.md5()
        md5.update(self.password.encode("utf-8"))
        return md5.hexdigest()
    
    def get_cookies(self):
            url = "https://www.tianyancha.com/cd/login.json"
            
            payload = {
                'mobile': self.phone_number,
                'cdpassword':self.encrypt_passwd(),
                'loginway': "PL",
                'autoLogin': False,
            }
            x = self.get_validate()
            if x:
                payload.update(x)
                #print(payload)
            else:
                print("wrong")
                raise Exception("stop here")

            resp = self.session.post(url=url, data=json.dumps(payload), headers=self.headers)
            print(resp.json())
            response = resp.json()
            cookies = {}
            for key,value in self.session.cookies.items():
                cookies[key] = value
            cookies["auth_token"] = response.get('data').get("token")
            return cookies
        
        
        
if __name__ == '__main__':
    cookies = Login()
    cookies.get_cookies()