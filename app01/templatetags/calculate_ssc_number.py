#!/usr/bin/env python
# -*-coding:utf-8 -*-

def calculate_ssc_number_func_1():
    print('calculate_ssc_number_func_1 xxxx')

from app01.templatetags import calculate_ssc_sixing
from app01.templatetags import calculate_ssc_housan
from app01.templatetags import calculate_ssc_zhongsan

# calculate_ssc_sixing.sixing_calcaulate(20191015044)

def get_sixing_danma(qihao):

    if isinstance(qihao,str):
        qihao = int(qihao)

    danma_dict = calculate_ssc_sixing.sixing_calcaulate(qihao)
    print('qihao,sixing',qihao,danma_dict)

    return danma_dict

def get_zhongsan(qihao):

    if isinstance(qihao,str):
        qihao = int(qihao)

    zhongsan_dict = calculate_ssc_zhongsan.zhongsan_calcaulate(qihao)
    print('qihao,zhongsan',qihao,zhongsan_dict)

    return zhongsan_dict

def get_housan(qihao):

    if isinstance(qihao,str):
        qihao = int(qihao)

    housan_dict = calculate_ssc_housan.housan_calcaulate(qihao)
    print('qihao,housan',qihao,housan_dict)

    return housan_dict

if __name__ == '__main__':
    pass




