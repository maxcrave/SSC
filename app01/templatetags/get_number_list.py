#!/usr/bin/env python
# -*-coding:utf-8 -*-

import collections
import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta


def get_pre_numbers(end_qihao, pre=20):
    ''' 获取当前期号 往前推 pre = 20期 号码 '''

    url = 'https://zst.cjcp.com.cn/cjwssc/view/ssc_zst5-ssc.html'
    SSC_NUMBER_DICT = collections.OrderedDict()

    if not isinstance(end_qihao, str):
        end_qihao_str = str(end_qihao)
    else:
        end_qihao_str = end_qihao

    qihao_str = end_qihao_str[-3:]
    qihao_int = int(qihao_str)


    if qihao_int >= pre:
        endqi = int(end_qihao_str)
        startqi = endqi - pre + 1
    else:
        riqi_day = end_qihao_str[-5:-3]
        riqi_month = end_qihao_str[-7:-5]
        riqi_year = end_qihao_str[:4]
        today = datetime(year=int(riqi_year),month=int(riqi_month),day=int(riqi_day))

        start_qi_date = today - timedelta(days=1, hours=0, minutes=0)
        start_qi_date_str = start_qi_date.strftime('%Y%m%d')

        startqi = qihao_int - pre + 60
        startqi = int(start_qi_date_str + '0' + str(startqi))
        endqi = int(end_qihao_str)

    payloads = {'startqi': startqi, 'endqi': endqi, 'searchType': 9}
    response = requests.post(url, payloads)

    soup = BeautifulSoup(response.text, features='html.parser')
    tags = soup.find(name='tbody', attrs={'id': 'pagedata'}, recursive=True)

    tr_tags = tags.find_all(name='tr')

    for item in tr_tags:
        tr_block = item.find_all(name='td')
        se = tr_block[1].get_text()
        qi = tr_block[2].get_text()
        SSC_NUMBER_DICT.update({se: qi,})

    return SSC_NUMBER_DICT


'''
data = {'startqi':20191015001,'endqi':20191015020,'searchType':9}
response =requests.post(url,data)

soup = BeautifulSoup(response.text, features='html.parser')
tags = soup.find(name='tbody', attrs={'id': 'pagedata'}, recursive=True)

tr_tags = tags.find_all(name='tr')

for item in tr_tags:
    tr_block = item.find_all(name='td')
    se = tr_block[1].get_text()
    qi = tr_block[2].get_text()
    SSC_NUMBER_DICT.update({se: qi,})

'''

if __name__ =='__main__':

    SSC_NUMBER_DICT = get_pre_numbers('20191015032')
    print(SSC_NUMBER_DICT)