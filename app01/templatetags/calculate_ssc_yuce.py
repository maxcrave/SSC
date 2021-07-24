#!/usr/bin/env python
# -*-coding:utf-8 -*-

from django import template
from django.utils.safestring import mark_safe
import os
import json,collections
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

    html = ''''''

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

    from app01.templatetags import show_number_sixing
    return show_number_sixing.check_times(seq)

####

from app01.templatetags import calculate_ssc_number

# @register.simple_tag
# def check_sixing_danma_1(qihao_str, number_str):
#     number_str = number_str[1:]
#     html = ''''''
#
#     danma_dict = calculate_ssc_number.get_sixing_danma(qihao_str)
#
#     for danma_str, all_counts in danma_dict.items():
#
#         good = False
#         for i in danma_str:
#             if i in number_str:
#                 good = True
#                 html += '''<td class="good">{}</td><td class="blank_num">'''.format(danma_str)
#                 break
#         if not good:
#             html += '''<td class="bad">{}</td><td class="blank_num">'''.format(danma_str)
#
#     return mark_safe(html)


# @register.simple_tag
# def check_zhongsan(qihao_str, number_str):
#     number_str = number_str[1:-1]
#     html = ''''''
#
#     zhongsan_dict = calculate_ssc_number.get_zhongsan(qihao_str)
#
#     for danma_str, all_counts in zhongsan_dict.items():
#         good = False
#         for i in danma_str:
#             if i in number_str:
#                 good = True
#                 html += '''<td class="good">{}</td>'''.format(danma_str)
#                 break
#         if not good:
#             html += '''<td class="bad">{}</td>'''.format(danma_str)
#
#     return mark_safe(html)

# @register.simple_tag
# def check_housan(qihao_str, number_str):
#     number_str = number_str[2:]
#     html = ''''''
#
#     hongsan_dict = calculate_ssc_number.get_housan(qihao_str)
#
#     for danma_str, all_counts in hongsan_dict.items():
#         good = False
#         for i in danma_str:
#             if i in number_str:
#                 good = True
#                 html += '''<td class="good">{}</td>'''.format(danma_str)
#                 break
#         if not good:
#             html += '''<td class="bad">{}</td>'''.format(danma_str)
#
#     print('>>>>>>>>>>>>>>')
#
#     check_housan_test(qihao_str, number_str)
#
#     return mark_safe(html)

#+++++++++++++++++++++

@register.simple_tag
def check_housan(qihao_str, number_str):


    dire_path = os.path.join(os.path.abspath('.'), 'app01', 'ssc_number_file')
    file_path = os.path.join(dire_path, 'ssc_dict_json.txt')

    with open(os.path.abspath(file_path), 'r') as fp:
        load_dict = json.load(fp, object_pairs_hook=collections.OrderedDict)

    analyse_1 = check_value(qihao_str, load_dict, 20)
    analyse_2 = check_value(qihao_str, load_dict, 10)

    result = regulation_1(analyse_1, analyse_2)

    number_str = number_str[2:]
    html = ''''''

    for i in number_str:
        if i in result['best']['result_rule']:
            html += '''<td class="good">{}</td>'''.format(result['best']['result_rule'])
            return mark_safe(html)

    html += '''<td class="bad">{}</td>'''.format(result['best']['result_rule'])
    return mark_safe(html)

def check_value(seq,load_dict,n):
    qihao = int(seq)
    analyse_1 = collections.OrderedDict()
    for i in range(n):
        qihao -= 1
        if str(qihao)[-3:] == '000':
            qihao = str(qihao)[:-3] + '288'
            qihao = int(qihao)
        analyse_1[str(qihao)] = load_dict.get(str(qihao),'98765')
    # print(analyse_1)
    return analyse_1

def regulation_1(analyse_1,analyse_2,n=10):
    rule_dict = {
        'a':['01234','56789'],
        'b':['02468','13579'],
        'c':['04689','12357'],
    }

    best_choice = {}
    best_choice['best'] = {
        'm_score': 0,
        'vibrate_score': 0,
        'result_rule': '',
    }
    for k,v in rule_dict.items():
        m_score, vibrate_score, result_rule = single_regulation_check(analyse_1,analyse_2,v[0],v[1],10)
        if m_score > best_choice['best']['m_score']:
            best_choice['best'] = {
                'm_score':m_score,
                'vibrate_score':vibrate_score,
                'result_rule':result_rule,
            }
        elif m_score == best_choice['best']['m_score']:
            if vibrate_score < best_choice['best']['vibrate_score']:
                best_choice['best'] = {
                    'm_score': m_score,
                    'vibrate_score': vibrate_score,
                    'result_rule': result_rule,
                }
        # print(m_score,vibrate_score,result_rule,'========')
    # print('best_choice',best_choice)

    return best_choice

def single_regulation_check(analyse_1,analyse_2,rule_1_left,rule_1_right,n=10):

    l_score = 0
    r_score = 0
    for k, v in analyse_1.items():
        a_count = 0
        d_count = 0
        check_list = v[-3:]
        for i in check_list:
            if i in rule_1_left:
                a_count += 1
        for i in check_list:
            if i in rule_1_right:
                d_count += 1

        if a_count == 3:
            l_score += 1
        if d_count == 3:
            r_score += 1
    m_score = n - l_score - r_score

    vibrate_score = 0
    like_left = 0
    like_right = 0
    for k,v in analyse_2.items():
        inner_a_count = 0
        inner_d_count = 0
        check_list = v[-3:]
        for i in check_list:
            if i in rule_1_left:
                inner_a_count += 1
        for i in check_list:
            if i in rule_1_right:
                inner_d_count += 1
        if inner_a_count == 3:
            vibrate_score += 1
        if inner_d_count == 3:
            vibrate_score += 1

        # print('--',v,inner_a_count,inner_d_count)
        if inner_a_count == 3:
            like_left += inner_a_count
        if inner_d_count == 3:
            like_right += inner_d_count

    if like_left >= like_right:
        result_rule = rule_1_left
    else:
        result_rule = rule_1_right

    # print(vibrate_score,like_left,like_right,'<<<')

    return m_score,vibrate_score,result_rule


#+++++++++++++++++++++

@register.simple_tag
def check_zhongsan(qihao_str, number_str):


    dire_path = os.path.join(os.path.abspath('.'), 'app01', 'ssc_number_file')
    file_path = os.path.join(dire_path, 'ssc_dict_json.txt')

    with open(os.path.abspath(file_path), 'r') as fp:
        load_dict = json.load(fp, object_pairs_hook=collections.OrderedDict)

    analyse_1 = check_value_zhongsan(qihao_str, load_dict, 20)
    analyse_2 = check_value_zhongsan(qihao_str, load_dict, 10)

    print(qihao_str)
    result = regulation_1_zhongsan(analyse_1, analyse_2)

    number_str = number_str[1:-1]
    html = ''''''

    for i in number_str:
        if i in result['best']['result_rule']:
            html += '''<td class="good">{}</td>'''.format(result['best']['result_rule'])
            return mark_safe(html)

    html += '''<td class="bad">{}</td>'''.format(result['best']['result_rule'])
    return mark_safe(html)

def check_value_zhongsan(seq,load_dict,n):
    qihao = int(seq)
    analyse_1 = collections.OrderedDict()
    for i in range(n):
        qihao -= 1
        if str(qihao)[-3:] == '000':
            qihao = str(qihao)[:-3] + '288'
            qihao = int(qihao)
        analyse_1[str(qihao)] = load_dict.get(str(qihao),'98765')   #<-----------------
    # print(analyse_1)
    return analyse_1

def regulation_1_zhongsan(analyse_1,analyse_2,n=10):
    rule_dict = {
        'a':['01234','56789'],
        'b':['02468','13579'],
        'c':['04689','12357'],
    }

    best_choice = {}
    best_choice['best'] = {
        'm_score': 0,
        'vibrate_score': 0,
        'result_rule': '',
    }
    for k,v in rule_dict.items():
        m_score, vibrate_score, result_rule = single_regulation_check_zhongsan(analyse_1,analyse_2,v[0],v[1],10)
        if m_score > best_choice['best']['m_score']:
            best_choice['best'] = {
                'm_score':m_score,
                'vibrate_score':vibrate_score,
                'result_rule':result_rule,
            }
        elif m_score == best_choice['best']['m_score']:
            if vibrate_score < best_choice['best']['vibrate_score']:
                best_choice['best'] = {
                    'm_score': m_score,
                    'vibrate_score': vibrate_score,
                    'result_rule': result_rule,
                }
        print(m_score,vibrate_score,result_rule,'========')
    print('best_choice',best_choice)

    return best_choice

def single_regulation_check_zhongsan(analyse_1,analyse_2,rule_1_left,rule_1_right,n=10):

    l_score = 0
    r_score = 0
    for k, v in analyse_1.items():
        a_count = 0
        d_count = 0
        check_list = v[1:-1]
        for i in check_list:
            if i in rule_1_left:
                a_count += 1
        for i in check_list:
            if i in rule_1_right:
                d_count += 1

        if a_count == 3:
            l_score += 1
        if d_count == 3:
            r_score += 1
    m_score = n - l_score - r_score

    vibrate_score = 0
    like_left = 0
    like_right = 0
    for k,v in analyse_2.items():
        inner_a_count = 0
        inner_d_count = 0
        check_list = v[1:-1]
        for i in check_list:
            if i in rule_1_left:
                inner_a_count += 1
        for i in check_list:
            if i in rule_1_right:
                inner_d_count += 1
        if inner_a_count == 3:
            vibrate_score += 1
        if inner_d_count == 3:
            vibrate_score += 1

        # print('--',v,inner_a_count,inner_d_count)
        if inner_a_count == 3:
            like_left += inner_a_count
        if inner_d_count == 3:
            like_right += inner_d_count

    if like_left >= like_right:
        result_rule = rule_1_left
    else:
        result_rule = rule_1_right

    # print(vibrate_score,like_left,like_right,'<<<')

    return m_score,vibrate_score,result_rule

#-----

@register.simple_tag
def check_sixing_danma_1(qihao_str, number_str):
    print('----',qihao_str, number_str)

    dire_path = os.path.join(os.path.abspath('.'), 'app01', 'ssc_number_file')
    file_path = os.path.join(dire_path, 'ssc_dict_json.txt')

    with open(os.path.abspath(file_path), 'r') as fp:
        load_dict = json.load(fp, object_pairs_hook=collections.OrderedDict)

    print('!!!!!!!!!!!!!!!!!!!!!!')
    analyse_1 = check_value_zhongsan(qihao_str, load_dict, 8)
    analyse_2 = check_value_zhongsan(qihao_str, load_dict, 8)
    print(analyse_1,analyse_2)
    best_choice = regulation_danma(analyse_1, analyse_2)

    number_str = number_str[1:]
    html_1 = '''<td class="bad">{}</td><td class="blank_num">'''.format(best_choice['best_1']['result_rule'])
    html_2 = '''<td class="bad">{}</td><td class="blank_num">'''.format(best_choice['best_2']['result_rule'])

    for i in number_str:
        if i in best_choice['best_1']['result_rule']:
            html_1 = '''<td class="good">{}</td><td class="blank_num">'''.format(best_choice['best_1']['result_rule'])
            break

    for i in number_str:
        if i in best_choice['best_2']['result_rule']:
            html_2 = '''<td class="good">{}</td><td class="blank_num">'''.format(best_choice['best_2']['result_rule'])
            break

    html = html_1 + html_2
    return mark_safe(html)

def regulation_danma(analyse_1,analyse_2,n=10):
    rule_dict = {
        'a': ['2457',],
        'b': ['1368',],
        'c': ['1248',],
        'd': ['0369',],
        'e': ['1457',],
        'f': ['1458',],
        'g': ['0189',],
    }

    best_choice = {}
    best_choice['best_1'] = {
        'm_score': 0,
        'inner_score': 0,
        'result_rule': '',
    }
    best_choice['best_2'] = {
        'm_score': 0,
        'inner_score': 0,
        'result_rule': '',
    }


    for k, v in rule_dict.items():
        m_score, inner_score, result_rule = danma_regulation_check(analyse_1, analyse_2, v[0], 10)
        print(m_score, inner_score, result_rule)
        if m_score > best_choice['best_1']['m_score']:
            best_choice['best_2'] = {
                'm_score': best_choice['best_1']['m_score'],
                'inner_score': best_choice['best_1']['inner_score'],
                'result_rule': best_choice['best_1']['result_rule'],
            }

            best_choice['best_1'] = {
                'm_score': m_score,
                'inner_score': inner_score,
                'result_rule': result_rule,
            }
        elif m_score == best_choice['best_1']['m_score']:
            if m_score > best_choice['best_2']['m_score'] and inner_score >= best_choice['best_1']['inner_score']:
                best_choice['best_2'] = {
                    'm_score': best_choice['best_1']['m_score'],
                    'inner_score': best_choice['best_1']['inner_score'],
                    'result_rule': best_choice['best_1']['result_rule'],
                }
                best_choice['best_1'] = {
                    'm_score': m_score,
                    'inner_score': inner_score,
                    'result_rule': result_rule,
                }
            elif m_score > best_choice['best_2']['m_score'] and inner_score < best_choice['best_1']['inner_score']:
                best_choice['best_2'] = {
                    'm_score': m_score,
                    'inner_score': inner_score,
                    'result_rule': result_rule,
                }
            elif inner_score > best_choice['best_1']['inner_score']:
                best_choice['best_2'] = {
                    'm_score': best_choice['best_1']['m_score'],
                    'inner_score': best_choice['best_1']['inner_score'],
                    'result_rule': best_choice['best_1']['result_rule'],
                }
                best_choice['best_1'] = {
                    'm_score': m_score,
                    'inner_score': inner_score,
                    'result_rule': result_rule,
                }
        elif m_score > best_choice['best_2']['m_score'] and m_score <= best_choice['best_1']['m_score']:
            best_choice['best_2'] = {
                'm_score': m_score,
                'inner_score': inner_score,
                'result_rule': result_rule,
            }

    print(best_choice)
    return best_choice

def danma_regulation_check(analyse_1,analyse_2,rule,n=10):

    m_score = 0
    inner_score = 0
    for k,v in analyse_1.items():
        for i in v[1:]:
            if i in rule:
                m_score += 1
                break
    Flag = True
    for k, v in analyse_2.items():
        for i in v[1:]:
            if i in rule:
                inner_score += 1
                Flag = False
                break
            if not Flag:
                inner_score = 0

    return m_score,inner_score,rule

# ==============

@register.simple_tag
def yuce_danma(qihao_str):
    qihao_list = qihao_str.split('-')
    qihao_str = ''.join(qihao_list)

    dire_path = os.path.join(os.path.abspath('.'), 'app01', 'ssc_number_file')
    file_path = os.path.join(dire_path, 'ssc_dict_json.txt')

    with open(os.path.abspath(file_path), 'r') as fp:
        load_dict = json.load(fp, object_pairs_hook=collections.OrderedDict)

    analyse_1 = check_value_zhongsan(qihao_str, load_dict, 8)
    analyse_2 = check_value_zhongsan(qihao_str, load_dict, 8)

    best_choice = regulation_danma(analyse_1, analyse_2)
    html = """<td class="">{}</td>
                <td class="blank_num"></td>
                <td class="">{}</td>
                <td class="blank_num"></td>""".format(best_choice['best_1']['result_rule'],best_choice['best_2']['result_rule'])

    return mark_safe(html)

@register.simple_tag
def yuce_zhongsan(qihao_str):
    qihao_list = qihao_str.split('-')
    qihao_str = ''.join(qihao_list)

    dire_path = os.path.join(os.path.abspath('.'), 'app01', 'ssc_number_file')
    file_path = os.path.join(dire_path, 'ssc_dict_json.txt')

    with open(os.path.abspath(file_path), 'r') as fp:
        load_dict = json.load(fp, object_pairs_hook=collections.OrderedDict)

    analyse_1 = check_value_zhongsan(qihao_str, load_dict, 20)
    analyse_2 = check_value_zhongsan(qihao_str, load_dict, 10)

    print(qihao_str)
    result = regulation_1_zhongsan(analyse_1, analyse_2)
    html = """<td class="">{}</td>
                <td class="blank_num"></td>""".format(result['best']['result_rule'])

    return mark_safe(html)

@register.simple_tag
def yuce_housan(qihao_str):
    qihao_list = qihao_str.split('-')
    qihao_str = ''.join(qihao_list)

    dire_path = os.path.join(os.path.abspath('.'), 'app01', 'ssc_number_file')
    file_path = os.path.join(dire_path, 'ssc_dict_json.txt')

    with open(os.path.abspath(file_path), 'r') as fp:
        load_dict = json.load(fp, object_pairs_hook=collections.OrderedDict)

    analyse_1 = check_value(qihao_str, load_dict, 20)
    analyse_2 = check_value(qihao_str, load_dict, 10)

    result = regulation_1(analyse_1, analyse_2)

    html = """<td class="">{}</td>
                <td class="blank_num"></td>""".format(result['best']['result_rule'])

    return mark_safe(html)