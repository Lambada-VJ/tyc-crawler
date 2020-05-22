# -*- coding: utf-8 -*-
"""
Created on Fri May 22 15:19:31 2020

@author: VJ
"""

import requests
from lxml import etree
import pandas as pd
from login import *
from get_urls import *

##### 企业详情页
def getCompanyInfo(url_all):
    compInfos = pd.DataFrame()
    for url in url_all:
        response = requests.get(url, headers=headers)
        content = response.content.decode('utf8')

        # 使用etree对html字符串解析
        html = etree.HTML(content)

        # 公司名称
        try:
            try:
                name = html.xpath('//div[@class="header"]/h1/text()')[0]
            except:
                name = "NaN"

            tbodys = html.xpath(
                '//div[@class="data-content"]/table[@class="table -striped-col -border-top-none -breakall"]')
            for tbody in tbodys:
                # 注册资本
                try:
                    regCapital = tbody.xpath('.//tr[1]/td[@width="308px"]//text()')[0]
                except:
                    regCapital = "NaN"
                # 实缴资本
                try:
                    actualCapital = tbody.xpath('.//tr[1]/td[4]//text()')[0]
                except:
                    actualCapital = "NaN"
                    # 成立日期
                try:
                    establishTime = tbody.xpath('.//tr[2]/td[@width="308px"]//text()')[0]
                except:
                    establishTime = "NaN"
                # 经营状态
                try:
                    regStatus = tbody.xpath('.//tr[2]/td[4]//text()')[0]
                except:
                    regStatus = "NaN"
                    # 统一社会信用代码
                try:
                    creditCode = tbody.xpath('.//tr[3]/td[@width="308px"]//text()')[0]
                except:
                    creditCode = "NaN"
                # 公司类型
                try:
                    companyOrgType = tbody.xpath('.//tr[5]/td[@width="308px"]//text()')[0]
                except:
                    companyOrgType = "NaN"
                # 行业
                try:
                    industry = tbody.xpath('.//tr[5]/td[4]//text()')[0]
                except:
                    industry = "NaN"
                # 核准日期
                try:
                    approvedTime = tbody.xpath('.//tr[6]/td[@width="308px"]//text()')[0]
                except:
                    approvedTime = "NaN"
                # 登记机关
                try:
                    regInstitute = tbody.xpath('.//tr[6]/td[4]//text()')[0]
                except:
                    regInstitute = "NaN"
                # 营业期限
                try:
                    businessTerm = tbody.xpath('.//tr[7]/td[@width="308px"]//text()')[0]
                except:
                    businessTerm = "NaN"
                # 纳税人资质
                try:
                    taxQuali = tbody.xpath('.//tr[7]/td[4]//text()')[0]
                except:
                    taxQuali = "NaN"
                # 人员规模
                try:
                    staffNumRange = tbody.xpath('.//tr[8]/td[@width="308px"]//text()')[0]
                except:
                    staffNumRange = "NaN"
                # 参保人数
                try:
                    socialStaffNum = tbody.xpath('.//tr[8]/td[4]//text()')[0]
                except:
                    socialStaffNum = "NaN"
                # 曾用名
                try:
                    historyNames = tbody.xpath('.//tr[9]/td[@width="308px"]//text()')[0]
                except:
                    historyNames = "NaN"
                    # 注册地址
                try:
                    regLocation = tbody.xpath('.//tr[10]/td[@colspan="4"]//text()')[0]
                except:
                    regLocation = "NaN"
                # 经营范围
                try:
                    businessScope = tbody.xpath('.//tr[11]/td[@colspan="4"]/span[@class]//text()')[0]
                except:
                    businessScope = "NaN"

                    # 所有信息整合到一个list中
                compInfo = [name, regCapital, actualCapital, establishTime, regStatus, creditCode, companyOrgType,
                            industry, approvedTime, regInstitute, businessTerm, taxQuali, staffNumRange, socialStaffNum,
                            historyNames, regLocation, businessScope]
                compInfos = compInfos.append(pd.DataFrame(compInfo).T)

        except:
            pass
    var = ['公司名', '注册资本', '实缴资本', '成立日期', '经营状态', '统一社会信用代码', '公司类型', '行业', '核准日期', '登记机关', '营业期限', '纳税人资质', '人员规模',
           '参保人数', '曾用名', '注册地址', '经营范围']
    compInfos.columns = var