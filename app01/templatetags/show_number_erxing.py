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

    start_number = number[:3]
    last_three = number[3:]

    html = '''
<span class="co_num">%s</span>
<span class="last_num co_num">%s</span>
'''%(start_number,last_three)

    return mark_safe(html)

@register.simple_tag
def shiwei_check(number):
    html = ''''''
    shiwei = number[3]

    if shiwei in '0369':
        html = '''
                <td class="shiwei"><span class="ball_2">0</span></td>
                <td class="shiwei">1</td>
                <td class="shiwei">1</td>
            '''
    elif shiwei in '147':
        html = '''
                <td class="shiwei">1</td>
                <td class="shiwei"><span class="ball_2">1</span></td>
                <td class="shiwei">1</td>
            '''
    else:
        html = '''
                <td class="shiwei">1</td>
                <td class="shiwei">1</td>
                <td class="shiwei"><span class="ball_2">2</span></td>
            '''

    return mark_safe(html)

@register.simple_tag
def gewei_check(number):
    html = ''''''
    gewei = number[4]

    if gewei in '0369':
        html = '''
                <td class="baiwei"><span class="ball_1">0</span></td>
                <td class="baiwei">1</td>
                <td class="baiwei">1</td>
            '''
    elif gewei in '147':
        html = '''
                <td class="baiwei">1</td>
                <td class="baiwei"><span class="ball_1">1</span></td>
                <td class="baiwei">1</td>
            '''
    else:
        html = '''
                <td class="baiwei">1</td>
                <td class="baiwei">1</td>
                <td class="baiwei"><span class="ball_1">2</span></td>
            '''

    return mark_safe(html)

@register.simple_tag
def number_type(number):

    html = '''
        <td class="num_type_1">组六</td>
        <td></td>
        <td></td>
    '''
    LAST_NUM = number[-3:]

    count = {}
    for i in LAST_NUM:
        count[i] = 0
    for i in LAST_NUM:
        count[i] += 1

    for k, v in count.items():
        if v > 1 and v <= 2 :

            html ='''
                <td></td>
                <td class="num_type_1">组三</td>
                <td></td>
            '''
            return mark_safe(html)
        elif v > 2:
            html = '''
                <td></td>
                <td></td>
                <td class="num_type_1">豹子</td>
            '''
        else:
            continue

    return mark_safe(html)

@register.simple_tag
def yu_zero(number):

    html = '''
    <td class="yu_0">%s</td>
    <td class="yu_0">%s</td>
    <td class="yu_0">%s</td>
    <td class="yu_0">%s</td>
    '''

    baiwei = number[2]
    shiwei = number[3]
    gewei = number[4]

    flag_0 = '1'
    flag_3 = '1'
    flag_6 = '1'
    flag_9 = '1'

    if baiwei in '0' or shiwei in '0' or gewei in '0':
        flag_0 = '<span class="ball_1">0</span>'
    elif baiwei in '3' or shiwei in '3' or gewei in '3':
        flag_3 = '<span class="ball_1">3</span>'
    elif baiwei in '6' or shiwei in '6' or gewei in '6':
        flag_6 = '<span class="ball_1">6</span>'
    elif baiwei in '9' or shiwei in '9' or gewei in '9':
        flag_9 = '<span class="ball_1">9</span>'

    html = html%(flag_0,flag_3,flag_6,flag_9,)

    return mark_safe(html)

@register.simple_tag
def yu_one(number):

    html = '''
    <td class="yu_1">%s</td>
    <td class="yu_1">%s</td>
    <td class="yu_1">%s</td>
    '''

    baiwei = number[2]
    shiwei = number[3]
    gewei = number[4]

    flag_1 = '1'
    flag_4 = '1'
    flag_7 = '1'

    if baiwei in '1' or shiwei in '1' or gewei in '1':
        flag_1 = '<span class="ball_1">1</span>'
    elif baiwei in '4' or shiwei in '4' or gewei in '4':
        flag_4 = '<span class="ball_1">4</span>'
    elif baiwei in '7' or shiwei in '7' or gewei in '7':
        flag_7 = '<span class="ball_1">7</span>'

    html = html%(flag_1,flag_4,flag_7)

    return mark_safe(html)

@register.simple_tag
def yu_two(number):

    html = '''
    <td class="yu_2">%s</td>
    <td class="yu_2">%s</td>
    <td class="yu_2">%s</td>
    '''

    baiwei = number[2]
    shiwei = number[3]
    gewei = number[4]

    flag_2 = '1'
    flag_5 = '1'
    flag_8 = '1'

    if baiwei in '2' or shiwei in '2' or gewei in '2':
        flag_2 = '<span class="ball_1">2</span>'
    elif baiwei in '5' or shiwei in '5' or gewei in '5':
        flag_5 = '<span class="ball_1">5</span>'
    elif baiwei in '8' or shiwei in '8' or gewei in '8':
        flag_8 = '<span class="ball_1">8</span>'

    html = html%(flag_2,flag_5,flag_8)

    return mark_safe(html)

@register.simple_tag
def check_BS(number):

    html = ''''''
    LAST_NUMBER = number[3:]
    count = 0

    for num in LAST_NUMBER:
        n = int(num)
        if n >= 5:
            count += 1

    if count == 2:
        html = '''
        <td></td>
        <td></td>
        <td class="tdbg">2:0</td>'''
    elif count == 1:
        html = '''
        <td></td>
        <td class="tdbg">1:1</td>
        <td></td>'''
    else:
        html = '''
        <td class="tdbg">0:2</td>
        <td></td>
        <td></td>'''

    return mark_safe(html)

@register.simple_tag
def check_qiou(number):

    html = ''''''
    LAST_NUMBER = number[3:]
    count = 0

    for num in LAST_NUMBER:
        if num in '13579':
            count += 1

    if count == 2:
        html = '''
        <td></td>
        <td></td>
        <td class="tdbg">2:0</td>'''
    elif count == 1:
        html = '''
        <td></td>
        <td class="tdbg">1:1</td>
        <td></td>'''
    else:
        html = '''
        <td class="tdbg">0:2</td>
        <td></td>
        <td></td>'''

    return mark_safe(html)

@register.simple_tag
def check_zhihe(number):

    html = ''''''
    LAST_NUMBER = number[3:]
    count = 0

    for num in LAST_NUMBER:
        if num in '12357':
            count += 1

    if count == 2:
        html = '''
        <td></td>
        <td></td>
        <td class="tdbg">2:0</td>'''
    elif count == 1:
        html = '''
        <td></td>
        <td class="tdbg">1:1</td>
        <td></td>'''
    else:
        html = '''
        <td class="tdbg">0:2</td>
        <td></td>
        <td></td>'''

    return mark_safe(html)

@register.simple_tag
def check_times(seq):

    from app01.templatetags import show_number_sixing
    return show_number_sixing.check_times(seq)