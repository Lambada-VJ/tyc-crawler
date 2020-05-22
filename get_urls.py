# -*- coding: utf-8 -*-
"""
Created on Fri May 22 15:01:17 2020

@author: VJ
"""

import requests
from lxml import etree
from login import *

class AllPages:
    def __init__(self):
        self.headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4100.3 Safari/537.36"
                        }
        self.url = 'https://www.tianyancha.com/'
        
    def get_AllCities(self):
        response = requests.get(self.url, headers = self.headers)
        content = response.content.decode('utf8')
        html = etree.HTML(content)
        urlsBase = html.xpath('//div[@class="right -scroll js-industry-container prov-list"]//a/@href')
        return urlsBase
    
    def get_AllPages(self):
        AllPages = []
        for url in self.get_AllCities():
            m, n = url.split('?')
            for i in range(0, 6):
                page = '/p' + '{}'.format(i) + '?'
                urlPage = m + page + n
                AllPages.append(urlPage)
        return AllPages 

if __name__ == '__main__':
    #cookies = Login()
    pages = AllPages()
    AllPages = pages.get_AllPages()
              
#####获取所有公司urls
def get_AllUrls(all_pages):
    headers = {
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4100.3 Safari/537.36"
              }
    cookie = cookies.get_cookies()
    print(cookie)
    AllUrls = []
    #for url in all_pages:
    response = requests.get(all_pages, headers=headers,cookies = cookie)
    content = response.content.decode('utf8')
    print(content)
       
    if content.status_code == 200:
        if '我们只是确认一下你不是机器人' in content.text:
            print('遭到反爬，需要文字点选验证')
        else:
            return content
    else:
        print('cookies失效')    
    html = etree.HTML(content)
    urlsOnepage = html.xpath('//div[@class="result-list sv-search-container"]//div[@class="header"]/a/@href')
    print(urlsOnepage)
    AllUrls.append(urlsOnepage)
    #print(content)
    return AllUrls