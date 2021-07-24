#!/usr/bin/env python
# -*-coding:utf-8 -*-

import collections
import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

def get_pre_number_list_infile(end_qihao, pre=20):
    ''' 获取当前期号 往前推 pre = 20期 号码 '''

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
        today = datetime(year=int(riqi_year), month=int(riqi_month), day=int(riqi_day))

        start_qi_date = today - timedelta(days=1, hours=0, minutes=0)
        start_qi_date_str = start_qi_date.strftime('%Y%m%d')

        startqi = qihao_int - pre + 60
        startqi = int(start_qi_date_str + '0' + str(startqi))
        endqi = int(end_qihao_str)

    payloads = {'startqi': startqi, 'endqi': endqi, 'searchType': 9}

    # dire_path = os.path.join(os.path.abspath('..') ,'ssc_number_file')
    dire_path = os.path.join(os.path.abspath('.'), 'app01','ssc_number_file')
    file_path = os.path.join(dire_path, 'number_file1.txt')


    with open(os.path.abspath(file_path), 'r') as f:
        file_content = f.read()
        content_start = str(startqi)+file_content.split(str(startqi))[1]
        #print(content_start)
        content_end = content_start.split(str(endqi))[0] + str(endqi) + content_start.split(str(endqi))[1][:7]

        for item in content_end.split('\n'):
            if item:
                se, q = item.split('-')
                SSC_NUMBER_DICT.update({se:q})

    return SSC_NUMBER_DICT

def get_pre_number_list(end_qihao, pre=20):
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

def get_one_pre_qihao_str(current_qihao):
    ''' 获取上一期的期号 （当前期数 -1 ）'''

    current_qihao_str = str(current_qihao)
    c_qihao_str = current_qihao_str[-3:]

    c_qihao_int = int(c_qihao_str)

    if c_qihao_int == 1:
        riqi_day = current_qihao_str[-5:-3]
        riqi_month = current_qihao_str[-7:-5]
        riqi_year = current_qihao_str[:4]
        today = datetime(year=int(riqi_year), month=int(riqi_month), day=int(riqi_day))

        start_qi_date = today - timedelta(days=1, hours=0, minutes=0)
        start_qi_date_str = start_qi_date.strftime('%Y%m%d')

        pre_qihao = 59
        pre_qihao_str = start_qi_date_str + '0' + str(pre_qihao)

    else:
        pre_qihao = int(c_qihao_str) - 1
        pre_qihao_str = current_qihao_str[:-3] +'{0:03d}'.format(pre_qihao)

    return pre_qihao_str

def zhongsan_check_in_number(item, regular):
    check_number = item[1][1:-1]
    for one_number in check_number:
        if one_number in regular:
            return True
    return False

def zhongsan_regular(ssc_pre_number_oderdict_list, check_list=None):

    if not check_list:
        check_list = ['01234', '56789', '13579', '02468', '12357', '04689']
    ssc_report = dict()
    for check_regular in check_list:
        ssc_report[check_regular] = 0

    for item in ssc_pre_number_oderdict_list.items():

        for check_regular in check_list:
            result = zhongsan_check_in_number(item, check_regular)
            if result:
                ssc_report[check_regular] += 1

    return ssc_report

def get_best_choice(pre_qihao, ssc_report, pre=10):
    ''' 获取 最优的 2项 ，超过2项继续 +pre 10,15,20,(只测超出项)'''

    best_value = 0
    best_choice = dict()
    regular_list = list()

    d = collections.defaultdict(list)
    for key, value in ssc_report.items():
        d[value].append(key)

    best_value = max(d)
    regular_list.extend(d[best_value])
    if len(regular_list) == 1:
        d.pop(best_value)
    elif len(regular_list) >= 2:
        ssc_orderdict = get_pre_number_list_infile(pre_qihao, pre=pre+5)
        ssc_report = zhongsan_regular(ssc_orderdict, check_list=regular_list)

        best_choice = get_best_choice(pre_qihao, ssc_report, pre=pre+5)

    print(ssc_report)
    if not best_choice:
        for i in regular_list:
            best_choice[i] = ssc_report[i]

    return best_choice




def zhongsan_calcaulate(current_qihao):

    pre_qihao = get_one_pre_qihao_str(current_qihao)

    ssc_orderdict = get_pre_number_list_infile(pre_qihao, pre=10)
    ssc_report = zhongsan_regular(ssc_orderdict)

    print(ssc_report)
    r = get_best_choice(pre_qihao, ssc_report, pre=10)
    print(r)

    return r

if __name__ == '__main__':

    zhongsan_calcaulate(20191015024)


