#!/usr/bin/env python
# -*-coding:utf-8 -*-

from django import template
from django.utils.safestring import mark_safe
import os
from SSC import settings
import datetime

register = template.Library()

@register.simple_tag
def show_qihao(seq):

    seq = str(seq)
    a = seq[0:-3]
    b = seq[-3:]
    temp = a + '-' + b

    return temp

@register.simple_tag
def show_number(number):

    start_number = number[:1]
    last_three = number[1:]

    html = '''
<span class="co_num">%s</span>
<span class="last_num co_num">%s</span>
'''%(start_number,last_three)

    return mark_safe(html)

@register.simple_tag
def check_sixing(number,c_list):

    hmtl = ''''''

    CO_NUMBER = number[1:]
    count = 0

    count_dict = {}
    for num in CO_NUMBER:
        if num in c_list:
            count_dict[num] = 0

    for num in CO_NUMBER:
        if num in c_list:
            count_dict[num] += 1
            count += 1

    if count == 0:
        html = '''<td class="bad">挂</td>'''
    elif count == 4:
        for k,v in count_dict.items():
            if v >= 2:
                html = '''<td class="good">中</td>'''
                break
            else:
                html = '''<td class="bad">挂</td>'''

    else:
        html = '''<td class="good">中</td>'''

    return mark_safe(html)

@register.simple_tag
def check_lastseq(seq,number,LAST_NUMBER):

    html = ''''''
    CO_NUMBER = number[1:]
    last_number = LAST_NUMBER.get(seq)

    if last_number:
        last_number = last_number[1:]
        count = 0

        count_dict = {}
        for num in CO_NUMBER:
            if num in last_number:
                count_dict[num] = 0

        for num in CO_NUMBER:
            if num in last_number:
                count_dict[num] += 1
                count += 1

        if count == 0:
            html = '''<td class="bad">挂</td>'''
        elif count == 4:
            for k, v in count_dict.items():
                if v >= 2:
                    html = '''<td class="good">中</td>'''
                    break
                else:
                    html = '''<td class="bad">挂</td>'''
        else:
            html = '''<td class="good">中</td>'''

    else:
        html = '''<td>None</td>'''

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