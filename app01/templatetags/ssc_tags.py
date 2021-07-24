#!/usr/bin/env python
# -*-coding:utf-8 -*-

from django import template
from django.utils.safestring import mark_safe
import os
from SSC import settings
register = template.Library()

@register.simple_tag
def show_qihao(seq):
    seq = str(seq)
    a = seq[0:-3]
    b = seq[-3:]
    temp = a + '-' + b

    return temp

@register.simple_tag
def produce_files(request,seq,SSC,SSC_cy):

    print('---->>')

    seq_next = SSC_cy.get(seq)
    seq_current = seq
    seq_current_num = SSC.get(seq_current)

    if not seq_next:
        return '√'
    else:
        file_path = os.path.join(settings.BASE_DIR,'app01','ssc_files',str(seq_next))
        Current_NUM = seq_current_num

        MIDDLE_NUM, LAST_NUM = Out_Mid_Lst_NUM(Current_NUM)

        SSC_SIZE, SSC_NUM_Buffer = COL_NUM(MIDDLE_NUM, LAST_NUM)

        if not os.path.exists(file_path):

            with open(file_path,'w') as f:
                f.write(SSC_NUM_Buffer)
        else:
            # print('已生成',seq)
            pass

    money = float('%.2f'%(SSC_SIZE*0.002))
    request.session['money'] = money

    return '√  ' + str(SSC_SIZE) + '注 %.2F, 元'%(SSC_SIZE*0.002)

def Out_Mid_Lst_NUM(Current_NUM):
    '''
    获得中3 后3号码
    :param Current_NUM:
    :return:
    '''
    M_NUM = Current_NUM[1:4]
    L_NUM = Current_NUM[-3:]

    # 1.判断后三
    Max_select = 0
    Min_select = 0
    for num in L_NUM:
        if int(num) >= 5:
            Max_select += 1
        else:
            Min_select += 1

    if Max_select > Min_select:
        LAST_NUM = '56789'
    else:
        LAST_NUM = '01234'

    # 1.判断中三
    Zhi_select = 0
    Ou_select = 0
    for num in M_NUM:
        if num in ['1', '3', '5', '7','9']:
            Zhi_select += 1
        else:
            Ou_select += 1

    if Zhi_select > Ou_select:
        MIDDLE_NUM = '13579'
    else:
        MIDDLE_NUM = '02468'
    # --------------------
    # for num in M_NUM:
    #     if int(num) >= 5:
    #         Zhi_select += 1
    #     else:
    #         Ou_select += 1
    #
    # if Zhi_select > Ou_select:
    #     MIDDLE_NUM = '56789'
    # else:
    #     MIDDLE_NUM = '01234'
    # ----------------------

    return MIDDLE_NUM, LAST_NUM

def COL_NUM(MIDDLE_NUM, LAST_NUM):
    ''' 返回生成号码 Size,Buffer'''

    SSC_NUM = []
    SSC_SIZE = 0

    for i in range(0,10000):
        num = '%04d'%i
        SSC_NUM.append(num)

    # print(SSC_NUM,len(SSC_NUM))

    # 1. 0189 / 123个
    temp = []
    for num in SSC_NUM:
        count = 0
        if num.count('0'):
            count += 1
        if num.count('1'):
            count += 1
        if num.count('8'):
            count += 1
        if num.count('9'):
            count += 1
        if count == 0 or count == 4:
            temp.append(num)

    SSC_NUM = list(set(SSC_NUM).difference(set(temp)))

    # 2. 1458 / 123个
    temp = []
    for num in SSC_NUM:
        count = 0
        if num.count('1'):
            count += 1
        if num.count('4'):
            count += 1
        if num.count('5'):
            count += 1
        if num.count('8'):
            count += 1
        if count == 0 or count == 4:
            temp.append(num)

    SSC_NUM = list(set(SSC_NUM).difference(set(temp)))

    SSC_NUM = sorted(SSC_NUM)

    # 3.中3:   取值12357
    temp = []
    for item in SSC_NUM:
        middle_three = item[0:3]
        for i in middle_three:
            if i in MIDDLE_NUM:
                temp.append(item)
                break
    SSC_NUM = temp

    # 3.后3:   取值56789
    temp = []
    for item in SSC_NUM:
        middle_three = item[1:4]
        for i in middle_three:
            if i in LAST_NUM:
                temp.append(item)
                break
    SSC_NUM = temp

    SSC_SIZE = len(SSC_NUM)

    SSC_NUM = ' '.join(SSC_NUM)


    SSC_NUM_Buffer = SSC_NUM

    return SSC_SIZE,SSC_NUM_Buffer

@register.simple_tag
def check_num(request,seq,SSC,SSC_cy):

    file_path = os.path.join(settings.BASE_DIR, 'app01', 'ssc_files', str(seq))

    if not os.path.exists(file_path):
        return mark_safe('<td class="no_data">没有数据</td>')
    else:
        Co_Number = SSC.get(seq)
        if Co_Number:

            Num_Buffer = None
            with open(file_path,'r') as f:
                Num_Buffer = f.read()
            if Co_Number[1:] in Num_Buffer:
                request.session['total'] -= (request.session['money'] * (1 * request.session['beitou']))
                request.session['total'] += (float('19.42') * (1 * request.session['beitou']))
                request.session['beitou'] = float(1)
                request.session['fuck'] = 0
                return mark_safe('<td class="red">中</td>')
            else:
                request.session['total'] -= (request.session['money'] * (1 * request.session['beitou']))
                request.session['beitou'] += 0
                request.session['fuck'] += 1

                request.session['max_fuck'] = max(request.session['fuck'],request.session['max_fuck'])

                return mark_safe('<td class="green">挂</td>')

        else:
            return mark_safe('<td class="no_data">没有数据</td>')

@register.simple_tag
def check_1(num,check_list):
    ''' 0189/1458 判断个数  #5608'''
    if num:
        Co_Number = num[1:]
        count = 0
        for n in Co_Number:
            if n in check_list:
                count += 1
        if count == 0 or count == 4:
            if count == 0:
                return mark_safe('<td class="green">挂</td>')
            if count == 4:
                # -- 同时出现
                s_count = 0
                for k in check_list:
                    if k in Co_Number:
                        s_count += 1
                if s_count == 4:
                    return mark_safe('<td class="green">挂</td>')
                else:
                    return mark_safe('<td class="red">中</td>')
        else:
            return mark_safe('<td class="red">中</td>')

@register.simple_tag
def rep_money(request):
    return '%.2f'%(request.session['total'])

@register.simple_tag
def money_detail(request):
    return '%.2f' % (request.session['total'])

@register.simple_tag
def beitou_detail(request):
    return '%.2f' % (request.session['beitou'])

@register.simple_tag
def before_detail(request):

    Before_money = '%.2f' % (request.session['total'] - (request.session['money'] * (1 * request.session['beitou'])))
    if float(Before_money) < 0:
        return mark_safe('<td class="warring">%s</td>'%(Before_money))
    else:
        return mark_safe('<td >%s</td>' % (Before_money))

@register.simple_tag
def num_detail(num):
    if num:
        LAST_NUM = num[-3:]

        count = {}
        for i in LAST_NUM:
            count[i] = 0
        for i in LAST_NUM:
            count[i] += 1

        for k,v in count.items():
            if v > 1:
                return mark_safe('<td class="bg-15"></td><td class="bg-14">组三</td>')
            else:
                continue

        return mark_safe('<td class="bg-14">组六</td><td class="bg-15"></td>')