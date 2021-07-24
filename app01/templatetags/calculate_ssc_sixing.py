#!/usr/bin/env python
# -*-coding:utf-8 -*-

import collections
import requests
import os
import re
from bs4 import BeautifulSoup


SSC_NUMBER = collections.OrderedDict()

SSC_CALCULATE_REPORT = dict()
SSC_CALCULATE_LIST = list()

def get_SSC_Number():

    URL = 'https://zst.cjcp.com.cn/cjwssc/view/ssc_zst5-ssc-0-3-59.html'
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, features='html.parser')
    tags = soup.find(name='tbody', attrs={'id': 'pagedata'}, recursive=True)

    tr_tags = tags.find_all(name='tr')

    for item in tr_tags:
        tr_block = item.find_all(name='td')
        se = tr_block[1].get_text()
        qi = tr_block[2].get_text()
        SSC_NUMBER.update({se: qi,})

    return

def number_put_in_list():

    for ssc_item in SSC_NUMBER.items():

        SSC_CALCULATE_LIST.append(ssc_item)
        if len(SSC_CALCULATE_LIST) == 10:
            number_calcaulate()

def number_calcaulate():

    check_list = ['0189', '1458', '1457', '0369', '1248', '1368', '2457']
    for check_regular in check_list:
        SSC_CALCULATE_REPORT[check_regular] = 0

    for item in SSC_CALCULATE_LIST:
        '''
            result_0189 = ssc_check_in_number(item, '0189')
            SSC_CALCULATE_REPORT['0189'] = 0
            if result_0189:
                SSC_CALCULATE_REPORT['0189'] += 1
        '''

        for check_regular in check_list:
            result = ssc_check_in_number(item, check_regular)
            if result:
                SSC_CALCULATE_REPORT[check_regular] += 1

    print('----')
    print(SSC_CALCULATE_LIST)
    print(SSC_CALCULATE_REPORT)

    return SSC_CALCULATE_LIST.pop(0)

def ssc_check_in_number(item, regular):
    check_number = item[1][1:]
    for one_number in check_number:
        if one_number in regular:
            return True

    return False

#########


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

def sixing_regular(ssc_pre_number_oderdict_list, check_list=None):

    if not check_list:
        check_list = ['0189', '1458', '1457', '0369', '1248', '1368', '2457']
    # if isinstance(check_list,dict):
    #     temp = []
    #     for key,value in check_list.items():
    #         temp.append(key)
    #     check_list = temp

    ssc_report = dict()
    for check_regular in check_list:
        ssc_report[check_regular] = 0

    for item in ssc_pre_number_oderdict_list.items():

        for check_regular in check_list:
            result = ssc_check_in_number(item, check_regular)
            if result:
                ssc_report[check_regular] += 1


    return ssc_report

######################################    失效    #########################################
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


    elif len(regular_list) >= 3:
        ssc_orderdict = get_pre_number_list_infile(pre_qihao, pre=pre+5)
        ssc_report = sixing_regular(ssc_orderdict, check_list=regular_list)
        print('rrrr',ssc_report)
        best_choice = get_best_choice(pre_qihao, ssc_report, pre=pre+5)

    if not best_choice:
        for i in regular_list:
            best_choice[i] = ssc_report[i]

    return best_choice
##########################################################################################


def get_best_regular(pre_qihao, ssc_report, pre=10):

    ''' {'1458': 9, '0369': 9, '1368': 9, '1248': 9, '1457': 9, '2457': 8, '0189': 8} '''

    d = collections.defaultdict(list)
    for regular, count in ssc_report.items():
        d[count].append(regular)

    regulars = len(d[max(d)])
    best_regulars = list()
    best_regulars.extend(d[max(d)])  # ['1457', '2457']
    print('best_regulars',best_regulars,len(best_regulars))
    if regulars == 1:
        # 最先选出的和最后选的检测期数会不同！
        best_choice = dict()
        for t in best_regulars:
            best_choice[t] = max(d)
            ssc_report.pop(t)

        # 产生 check_list
        d = collections.defaultdict(list)
        for regular, count in ssc_report.items():
            d[count].append(regular)

        regulars = len(d[max(d)])
        best_regulars = list()
        best_regulars.extend(d[max(d)])
        check_list = best_regulars
        # # # # # #

        one_regular = get_best_regular_one(pre_qihao, ssc_report, check_list, pre=pre)

        best_choice.update(one_regular)
        return best_choice

    elif regulars == 2:
        best_choice = dict()
        for t in best_regulars:
            best_choice[t] = max(d)

        return best_choice

    elif regulars > 2 :
        best_choice = dict()
        for t in best_regulars:
            best_choice[t] = max(d)
        ssc_report = best_choice
        r = get_best_regular_two(pre_qihao, ssc_report, check_list=best_regulars, pre=pre)

        return r

def get_best_regular_one(pre_qihao, ssc_report, check_list,pre=10):

    ssc_orderdict = get_pre_number_list_infile(pre_qihao, pre=pre + 5)
    ssc_report = sixing_regular(ssc_orderdict, check_list=check_list)

    d = collections.defaultdict(list)
    for regular, count in ssc_report.items():
        d[count].append(regular)

    regulars = len(d[max(d)])
    best_regulars = list()
    best_regulars.extend(d[max(d)])  # ['1457', '2457']


    if regulars == 1:
        best_choice = dict()
        for t in best_regulars:
            best_choice[t] = max(d)
            ssc_report.pop(t)
        return best_choice
    else:
        r = get_best_regular_one(pre_qihao, ssc_report, check_list=best_regulars,pre=pre + 5)
        return r

def get_best_regular_two(pre_qihao, ssc_report, check_list, pre=10):

    ssc_orderdict = get_pre_number_list_infile(pre_qihao, pre=pre + 5)
    ssc_report = sixing_regular(ssc_orderdict, check_list=check_list)

    r = get_best_regular(pre_qihao, ssc_report, pre=pre + 5)


    return r





def sixing_calcaulate(current_qihao):

    pre_qihao = get_one_pre_qihao_str(current_qihao)
    ssc_orderdict = get_pre_number_list_infile(pre_qihao, pre=5)
    ssc_report = sixing_regular(ssc_orderdict)
    print('current_qihao',ssc_report)

    r = get_best_regular(pre_qihao, ssc_report, pre=5)
    return r





if __name__ == '__main__':
    # get_SSC_Number()
    # print(SSC_NUMBER)
    #
    # number_put_in_list()

    r = sixing_calcaulate(20191015051)
    print(r)

    # get_pre_number_list_infile(20191015033)
    #r = get_pre_number_list(20191015033)
    #print(r)


    # k = {'1457': 9, '0189': 8, '2457': 9, '0369': 8, '1368': 8, '1248': 9, '1458': 9}
    # r = get_best_regular(get_one_pre_qihao_str(20191015033), k, pre=10)
    # print('----',r)