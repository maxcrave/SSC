#!/usr/bin/env python
# -*-coding:utf-8 -*-

from django import template
from django.utils.safestring import mark_safe
import os
from SSC import settings
import datetime
import json
import collections

register = template.Library()

@register.simple_tag
def show_qihao(seq):

    seq = str(seq)
    a = seq[0:-3]
    b = seq[-3:]
    temp = a + '-' + b

    return temp

@register.simple_tag
def show_number(request,number):

    if request.session['type'] == 'qian_san':
        start_number = number[:3]
        last_three = number[3:]
        html = '''
            <span class="co_num">%s</span>
            <span class="last_num co_num">%s</span>
            ''' % (start_number, last_three)
    elif request.session['type'] == 'zhong_san':
        start_number = number[:1]
        middle_three = number[1:-1]
        last_three = number[4]
        html = '''
        <span class="co_num">%s</span>
        <span class="last_num co_num">%s</span>
        <span class="co_num">%s</span>
        ''' % (start_number, middle_three, last_three)
    elif request.session['type'] == 'hou_san':
        start_number = number[:2]
        last_three = number[-3:]
        html = '''
            <span class="co_num">%s</span>
            <span class="last_num co_num">%s</span>
            ''' % (start_number, last_three)


    return mark_safe(html)

def type_number_split(request,number):
    ''' 前中后三 号码类型切割 '''
    if request.session['type'] == 'qian_san':
        return number[:3]
    elif request.session['type'] == 'zhong_san':
        return number[1:4]
    elif request.session['type'] == 'hou_san':
        return number[-3:]

def type_number_split_second(request,number):
    ''' 前中后二星 号码类型切割 '''
    if request.session['type'] == 'qian_san':
        return number[1:3]
    elif request.session['type'] == 'zhong_san':
        return number[2:4]
    elif request.session['type'] == 'hou_san':
        return number[-2:]

def get_yuce_danma(request,seq):
    return '0369'

def get_yuce_fivema(request,seq):
    """
    预测 5码
    :param qihao: 当前期号
    :param n:  选取 N 期,作为依据 计算
    :return:
    """

    n = request.session['pre_count']

    dire_path = os.path.join(os.path.abspath('.'), 'app01', 'ssc_number_file')
    file_path = os.path.join(dire_path, 'ssc_dict_json.txt')

    with open(os.path.abspath(file_path), 'r') as fp:
        load_dict = json.load(fp, object_pairs_hook=collections.OrderedDict)

    qihao = int(seq)
    analyse_1 = collections.OrderedDict()
    for i in range(n):
        qihao -= 1
        if str(qihao)[-3:] == '000':
            qihao = str(qihao)[:-3] + '288'
            qihao = int(qihao)
        analyse_1[str(qihao)] = type_number_split(request,load_dict.get(str(qihao), '999'))  # <-----------------

    count_list = collections.OrderedDict()
    for i in range(0,10):
        count_list[str(i)] = 0
    for k,v in analyse_1.items():
        for a in v:
            count_list[a] = count_list[a] + 1

    result_list = sorted(count_list.items(), key=lambda x: x[1] , reverse=True)
    result_fivema = ''

    for i in range(5):
        result_fivema += str(result_list[i][0])

    temp_list = list(result_fivema)
    temp_list.sort()
    result_fivema = "".join(temp_list)

    return result_fivema

def get_yuce_erxing(request,seq):
    """
    预测 6码
    :param qihao: 当前期号
    :param n:  选取 N 期,作为依据 计算
    :return:
    """

    # n = request.session['pre_count']
    n = 5

    dire_path = os.path.join(os.path.abspath('.'), 'app01', 'ssc_number_file')
    file_path = os.path.join(dire_path, 'ssc_dict_json.txt')

    with open(os.path.abspath(file_path), 'r') as fp:
        load_dict = json.load(fp, object_pairs_hook=collections.OrderedDict)

    qihao = int(seq)
    analyse_1 = collections.OrderedDict()
    for i in range(n):
        qihao -= 1
        if str(qihao)[-3:] == '000':
            qihao = str(qihao)[:-3] + '288'
            qihao = int(qihao)
        analyse_1[str(qihao)] = load_dict.get(str(qihao), '98765')  # <-----------------
        analyse_1[str(qihao)] = type_number_split_second(request, load_dict.get(str(qihao), '99'))

    count_list = collections.OrderedDict()
    for i in range(0,10):
        count_list[str(i)] = 0
    for k,v in analyse_1.items():
        for a in v:
            count_list[a] = count_list[a] + 1

    result_list = sorted(count_list.items(), key=lambda x: x[1] , reverse=True)
    result_erxing = ''

    for i in range(6):
        result_erxing += str(result_list[i][0])

    temp_list = list(result_erxing)
    temp_list.sort()
    result_erxing = "".join(temp_list)

    return result_erxing


@register.simple_tag
def calc_sanxing_danma(request,qihao,number):
    ''' 计算 后三胆码 '''

    result_number = type_number_split(request,number)
    calc_danma = get_yuce_danma(request,qihao)
    result_html = check_sanxing_danma(request,result_number,calc_danma)
    return result_html

@register.simple_tag
def calc_sanxing_fivema(request,qihao,number):
    ''' 计算 后三 5码 '''

    result_number = type_number_split(request,number)
    calc_fivema = get_yuce_fivema(request,qihao)
    result_html = check_sanxing_fivema(request,result_number,calc_fivema)
    return result_html

@register.simple_tag
def calc_erxing(request,qihao,number):
    ''' 计算 后二6码 '''

    result_number = type_number_split(request,number)[1:]
    calc_houer = get_yuce_erxing(request,qihao)
    result_html = check_erxing_danma(request,result_number,calc_houer)
    return result_html

@register.simple_tag
def calc_money(request):

    html = ''''''
    request.session['start_money'] -= 12

    if request.session['bad'] != 0:
        get_money = request.session['start_money']
        html = '''<td class="bad">{:.2f}</td>'''.format(get_money)
    else:
        request.session['start_money'] += 19.50
        get_money = request.session['start_money']

        html = '''<td class="good">{:.2f}</td>'''.format(get_money)

    request.session['bad'] = 0
    return mark_safe(html)


def check_sanxing_danma(request,number,calc_danma):
    """ 三星胆码出12

    :param number:  当期分割后得到的后三号码  XXX
    :param calc_danma: 计算获得预测得后三号码 0369/147/258
    :return:
    """
    html = ''''''

    count = 0

    count_dict = {}
    for num in number:
        if num in calc_danma:
            count_dict[num] = 0

    for num in number:
        if num in calc_danma:
            count += 1
            count_dict[num] += 1

    if count == 0:
        html = '''<td class="bad">{bad}</td>'''.format(bad=calc_danma)
        request.session['bad'] += 1
    elif count == 3:
        for k, v in count_dict.items():
            if v >= 2:
                html = '''<td class="good">{good}</td>'''.format(good=calc_danma)
                break
            else:
                html = '''<td class="bad">{bad}</td>'''.format(bad=calc_danma)
                request.session['bad'] += 1
    else:
        html = '''<td class="good">{good}</td>'''.format(good=calc_danma)


    return mark_safe(html)

def check_sanxing_fivema(request,number,calc_fivema):
    ''' （后）三5码出123 '''
    html = ''''''

    count = 0

    for num in number:
        if num in calc_fivema:
            count += 1

    if count >=1  :
        html = '''<td class="good">{good}</td>'''.format(good=calc_fivema)
    else:
        html = '''<td class="bad">{bad}</td>'''.format(bad=calc_fivema)
        request.session['bad'] += 1


    return mark_safe(html)

def check_erxing_danma(request,number,calc_houer):
    ''' (后)二 6码 '''
    html = ''''''

    count = 0

    for num in number:
        if num in calc_houer:
            count += 1

    if count >=1  :
        html = '''<td class="good">{good}</td>'''.format(good=calc_houer)
    else:
        html = '''<td class="bad">{bad}</td>'''.format(bad=calc_houer)
        request.session['bad'] += 1

    return mark_safe(html)

@register.simple_tag
def check_times(seq):
    html = '''<td></td>'''

    seq = str(seq)
    seq_no = seq[-3:]

    c_time = datetime.datetime.now()

    if seq_no == '001':
        c_time = c_time.replace(minute=5, hour=0)
        html = '''<td>%s</td>'''%(c_time.strftime('%H:%M'))
        return mark_safe(html)

    elif int(seq_no) >= 2 and int(seq_no) < 288:

        c_time = c_time.replace(minute=5, hour=0)
        m = int(seq_no)-1
        c_time = c_time + datetime.timedelta(minutes=5*m)
        html = '''<td>%s</td>''' % (c_time.strftime('%H:%M'))
        return mark_safe(html)

    elif int(seq_no) == 288:
        c_time = c_time.replace(minute=0, hour=0)
        html = '''<td>%s</td>''' % (c_time.strftime('%H:%M'))
        return mark_safe(html)

    return mark_safe(html)