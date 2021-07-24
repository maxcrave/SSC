from django.shortcuts import render,HttpResponse
import requests
from bs4 import BeautifulSoup
import collections
import json
import re
import datetime,time
import os
import copy

from django.views.decorators.cache import cache_page


SSC = collections.OrderedDict()

@cache_page(60 * 1)
def index(request):
    now_time = time.time()

    response = requests.get('https://chart.cp.360.cn/zst/getchartdata?lotId=255401&chartType=x5zh&spanType=0&span=30&r=0.22509768237038608#roll_132')
    # response = requests.get('http://chart.cp.360.cn/zst/getchartdata?lotId=255401&chartType=x5zh&spanType=0&span=1000&r=0.9090653652456879')
    # print(response.text)

    soup = BeautifulSoup(response.text,features='html.parser')

    tags = soup.find_all(name='tbody',attrs={'class':'zx5zh'},recursive=True)

    qi_list = []
    SSC_cy = collections.OrderedDict()

    for item in tags[0].children:
        se = item.find_all(name='td',attrs={'class':'tdbg_1'})
        if se:

            qi = se[0].get_text()
            qi = int(''.join(qi.split('-')))


            # if int(str(qi)[-3:]) in range(1,24):
            #     continue

            num = se[1].get_text()
            SSC.update({qi:num,})

            # ========
            qi_list.append(qi)


    # ---------- 添加下一期 期号:
    # response = requests.get('http://chart.cp.360.cn/int/qcurissue?LotID=255401&r=%s'%time.ctime())

    # rep = json.loads(response.text)
    next_seq = int('190321047')
    qi_list.append(next_seq)

    SSC[next_seq] = None

    # ----------- 构造映射
    qi_before_list = qi_list[1:]

    for i in range(len(qi_before_list)):
        SSC_cy[qi_list[i]] = qi_before_list[i]

    # print(SSC)
    #
    # print(SSC_cy)
    request.session['total'] = float(50)
    request.session['beitou'] = float(1)
    request.session['fuck'] = 0
    request.session['max_fuck'] = 0

    return render(request,'index.html',{'now_time':now_time,'SSC':SSC,'SSC_cy':SSC_cy})


SSC_NUMBER = collections.OrderedDict()

# SSCURL_detail = 'http://chart.cp.360.cn/zst/getchartdata?lotId=255401&chartType=x5zh&spanType=2&span=2018-06-26_2018-06-26&r=0.7200657716483869'
SSCURL_detail = 'https://chart.cp.360.cn/zst/getchartdata?lotId=255401&chartType=x5zh&spanType=1&span=1&r=0.11409514036972546#roll_132'

############################################################
''' 前 中 后 三分析'''

@cache_page(60 * 1)
def ssc_hou(request):


    '''  # ---------  过期URL
    response = requests.get(SSCURL_detail)
    soup = BeautifulSoup(response.text, features='html.parser')
    tags = soup.find_all(name='tbody', attrs={'class': 'zx5zh'}, recursive=True)
    for item in tags[0].children:
        se = item.find_all(name='td', attrs={'class': 'tdbg_1'})
        if se:
            qi = se[0].get_text()
            qi = int(''.join(qi.split('-')))

            num = se[1].get_text()
            SSC_NUMBER.update({qi: num,})

    print(SSC_NUMBER)
    '''

    SSC_NUMBER = get_SSC_Number()


    # ---------- 添加下一期 期号:
    last_no, last_num, LAST_NUMBER = get_last_number(SSC_NUMBER)
    next_seq = find_next_seq(last_no)

    nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

    return render(request,'ssc_housan.html',{'nowtime':nowtime,'SSC_NUMBER':SSC_NUMBER,'next_seq':next_seq})

@cache_page(60 * 1)
def ssc_zhong(request):

    '''
    response = requests.get(SSCURL_detail)
    soup = BeautifulSoup(response.text, features='html.parser')
    tags = soup.find_all(name='tbody', attrs={'class': 'zx5zh'}, recursive=True)
    for item in tags[0].children:
        se = item.find_all(name='td', attrs={'class': 'tdbg_1'})
        if se:
            qi = se[0].get_text()
            qi = int(''.join(qi.split('-')))

            num = se[1].get_text()
            SSC_NUMBER.update({qi: num,})
    '''
    SSC_NUMBER = get_SSC_Number()

    # ---------- 添加下一期 期号:
    last_no, last_num, LAST_NUMBER = get_last_number(SSC_NUMBER)
    next_seq = find_next_seq(last_no)

    nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

    return render(request,'ssc_zhongsan.html',{'nowtime':nowtime,'SSC_NUMBER':SSC_NUMBER,'next_seq':next_seq})

@cache_page(60 * 1)
def ssc_qian(request):

    '''
    response = requests.get(SSCURL_detail)
    soup = BeautifulSoup(response.text, features='html.parser')
    tags = soup.find_all(name='tbody', attrs={'class': 'zx5zh'}, recursive=True)
    for item in tags[0].children:
        se = item.find_all(name='td', attrs={'class': 'tdbg_1'})
        if se:
            qi = se[0].get_text()
            qi = int(''.join(qi.split('-')))

            num = se[1].get_text()
            SSC_NUMBER.update({qi: num,})
    '''
    SSC_NUMBER = get_SSC_Number()

    # ---------- 添加下一期 期号:
    last_no, last_num, LAST_NUMBER = get_last_number(SSC_NUMBER)
    next_seq = find_next_seq(last_no)

    nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

    return render(request,'ssc_qiansan.html',{'nowtime':nowtime,'SSC_NUMBER':SSC_NUMBER,'next_seq':next_seq})

############################################################

@cache_page(60 * 1)
def ssc_sixing(request):

    '''
    response = requests.get(SSCURL_detail)
    soup = BeautifulSoup(response.text, features='html.parser')
    tags = soup.find_all(name='tbody', attrs={'class': 'zx5zh'}, recursive=True)
    for item in tags[0].children:
        se = item.find_all(name='td', attrs={'class': 'tdbg_1'})
        if se:
            qi = se[0].get_text()
            qi = int(''.join(qi.split('-')))

            num = se[1].get_text()
            SSC_NUMBER.update({qi: num,})
    '''

    SSC_NUMBER = get_SSC_Number()  # 获取号码dict
    # SSC_NUMBER = get_HeNei_SSC(day=24,month=10,year=2020,hour=0)  # 河内5分彩

    last_no, last_num, LAST_NUMBER = get_last_number(SSC_NUMBER)

    next_seq = find_next_seq(last_no)

    nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

    ''' 测试用法
    from app01.templatetags import calculate_ssc_number
    calculate_ssc_number.calculate_ssc_number_func_1()
    '''

    return render(request,'ssc_sixing.html',{'nowtime':nowtime,
                                             'SSC_NUMBER':SSC_NUMBER,
                                             'LAST_NUMBER':LAST_NUMBER,
                                             'next_seq':next_seq,})


############################################################
''' 后三预测计算 Page'''

@cache_page(60 * 1)
def ssc_housan_yuce(request):

    # SSC_NUMBER = get_SSC_Number()  # 获取号码dict

    check_option = {
        'type': 2,
        'check_hour': 23,
        'start_hours': 8,
        'check_year': 2021,
        'check_month': 7,
        'check_day': 22,
    }
    check_SSC_files(**check_option)
    ssc_number_dict = Read_SSC_Number_From_Files(**check_option)

    SSC_NUMBER = ssc_number_dict

    dire_path = os.path.join(os.path.abspath('.'), 'app01', 'ssc_number_file')
    check_option = {
        'type': 2,
        'check_hour': 7,
        'start_hours': 0,
        'check_year': 2021,
        'check_month': 7,
        'check_day': 22,
    }

    temp_1 = copy.deepcopy(ssc_number_dict)
    check_SSC_files(**check_option)
    temp = Read_SSC_Number_From_Files(**check_option)
    temp_1.update(temp)

    with open(os.path.abspath(os.path.join(dire_path, 'ssc_dict_json.txt')), 'w+') as fp:
        fp.write(json.dumps(temp_1))



    last_no, last_num, LAST_NUMBER = get_last_number(SSC_NUMBER)

    next_seq = find_next_seq(last_no)

    nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

    request.session['type'] = 'zhong_san'
    request.session['pre_count'] = 8
    request.session['start_money'] = float(100)
    request.session['bad'] = 0
    request.session['good'] = 0

    return render(request,'ssc_housan_yuce.html',{'nowtime':nowtime,
                                             'SSC_NUMBER':SSC_NUMBER,
                                             'LAST_NUMBER':LAST_NUMBER,
                                             'next_seq':next_seq,})


############################################################


def get_last_number(SSC_NUMBER_DICT):
    ''' 获取前一期的号码 '''
    LAST_NUMBER = collections.OrderedDict()
    last_no = None  # 期号
    last_num = None
    for k, v in SSC_NUMBER_DICT.items():
        LAST_NUMBER[k] = last_num
        last_num = v
        last_no = k

    return last_no,last_num,LAST_NUMBER

def make_sscnumber(request):
    need_money = float(0)
    SSC_NUM_Buffer = None
    SSC_SIZE = 0
    filter_dict = {}

    if request.method == 'POST':
        danma_1 = request.POST.get('danma_1')
        danma_2 = request.POST.get('danma_2')
        m_num = request.POST.get('m_num')
        l_num = request.POST.get('l_num')

        filter_dict['胆码1'] = danma_1
        filter_dict['胆码2'] = danma_2
        filter_dict['中三5码'] = m_num
        filter_dict['后三5码'] = l_num

        All_number = produce_number()

        result_number = filter_danma(All_number,danma_1)
        result_number = filter_danma(result_number,danma_2)
        SSC_SIZE, SSC_NUM_Buffer = filter_MandL(result_number,m_num,l_num)

        need_money = float(SSC_SIZE * 0.002)

    else:
        pass

    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    return render(request,'ssc_make_number.html',{'nowtime':nowtime,
                                                  'need_money':need_money,
                                                  'SSC_NUM_Buffer':SSC_NUM_Buffer,
                                                  'SSC_SIZE':SSC_SIZE,
                                                  'filter_dict':filter_dict})

def produce_number():
    SSC_NUM = []
    for i in range(0,10000):
        num = '%04d'%i
        SSC_NUM.append(num)
    return SSC_NUM

def filter_danma(All_number,danma_1):
    SSC_NUMBER = []

    temp1 = []
    count = 0
    for number in All_number:
        for n in danma_1:
            count = number.count(n)
            if count >=1 :
                temp1.append(number)
                break

    # 过滤 1234情况
    SSC_NUMBER_DICT = {}
    for number in temp1:
        SSC_NUMBER_DICT[number] = {}
        for n in danma_1:
            SSC_NUMBER_DICT[number].update({n:number.count(n)})

    for number,v_dict in SSC_NUMBER_DICT.items():
        temp2_count = 0
        for k,v in v_dict.items():
            if v == 1:
                temp2_count += 1
        if temp2_count != 4:
            SSC_NUMBER.append(number)

    return sorted(SSC_NUMBER)

def filter_MandL(All_number,middle_number,last_number):

    # 3.中3:   取值12357
    temp = []
    for item in All_number:
        middle_three = item[0:3]
        for i in middle_three:
            if i in middle_number:
                temp.append(item)
                break

    SSC_NUM = temp

    # 3.后3:   取值56789
    temp = []
    for item in SSC_NUM:
        middle_three = item[1:4]
        for i in middle_three:
            if i in last_number:
                temp.append(item)
                break

    SSC_NUM = temp

    SSC_SIZE = len(SSC_NUM)

    SSC_NUM = ' '.join(SSC_NUM)
    SSC_NUM_Buffer = SSC_NUM

    return SSC_SIZE, SSC_NUM_Buffer

def find_next_seq(last_no):
    '''
    # ---------- 添加下一期 期号:
    '''
    next_seq = int(last_no) + 1
    temp = list(str(next_seq))
    temp.insert(8,'-')
    return ''.join(temp)

def make_sanxing(request):
    need_money = float(0)
    SSC_NUM_Buffer = None
    SSC_SIZE = 0
    filter_dict = {}

    if request.method == 'POST':
        danma_1 = request.POST.get('danma_1')
        last_three = request.POST.get('last_three')
        last_two = request.POST.get('last_two')

        filter_dict['后三胆码'] = danma_1
        filter_dict['后三5码'] = last_three
        filter_dict['后二6码'] = last_two

        SSC_SIZE, SSC_NUM_Buffer = filter_sanxing(danma_1,last_three,last_two)

        need_money = float(SSC_SIZE * 0.02)

    else:
        pass

    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    return render(request,'ssc_make_sanxing.html',{'nowtime':nowtime,
                                                   'need_money': need_money,
                                                   'SSC_NUM_Buffer': SSC_NUM_Buffer,
                                                   'SSC_SIZE': SSC_SIZE,
                                                   'filter_dict': filter_dict})

def filter_sanxing(danma,last_number,danma_2):
    SSC_NUM = []

    for i in range(0, 1000):
        num = '%03d' % i
        SSC_NUM.append(num)

    SSC_NUMBER = []

    temp1 = []
    for number in SSC_NUM:
        for i in danma:
            if i in number:
                temp1.append(number)
                break

    SSC_NUMBER_DICT = {}
    for number in temp1:
        SSC_NUMBER_DICT[number] = {}
        for i in danma:
            SSC_NUMBER_DICT[number].update({i: number.count(i)})

    for number, v_dict in SSC_NUMBER_DICT.items():
        temp2_count = 0
        for k, v in v_dict.items():
            if v == 1:
                temp2_count += 1
        if temp2_count != 3:
            SSC_NUMBER.append(number)

    SSC_NUMBER = sorted(SSC_NUMBER)

    temp2 = []

    for number in SSC_NUMBER:
        for i in last_number:
            if i in number:
                temp2.append(number)
                break

    SSC_NUMBER = sorted(temp2)

    temp3 = []
    for number in SSC_NUMBER:
        last_two = number[1:]
        for n in danma_2:
            if n in last_two:
                temp3.append(number)
                break

    SSC_NUMBER = sorted(temp3)
    SSC_SIZE = len(SSC_NUMBER)

    SSC_NUM = ' '.join(SSC_NUMBER)
    SSC_NUM_Buffer = SSC_NUM

    return SSC_SIZE,SSC_NUM_Buffer

@cache_page(60 * 1)
def ssc_erxing(request):

    '''
    response = requests.get(SSCURL_detail)
    soup = BeautifulSoup(response.text, features='html.parser')
    tags = soup.find_all(name='tbody', attrs={'class': 'zx5zh'}, recursive=True)
    for item in tags[0].children:
        se = item.find_all(name='td', attrs={'class': 'tdbg_1'})
        if se:
            qi = se[0].get_text()
            qi = int(''.join(qi.split('-')))

            num = se[1].get_text()
            SSC_NUMBER.update({qi: num,})
    '''
    SSC_NUMBER = get_SSC_Number()

    # ---------- 添加下一期 期号:
    last_no, last_num, LAST_NUMBER = get_last_number(SSC_NUMBER)
    next_seq = find_next_seq(last_no)

    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    return render(request,'ssc_erxing.html',{'nowtime':nowtime,'SSC_NUMBER':SSC_NUMBER,'next_seq':next_seq})

def get_SSC_Number(URL=None):

    ''' Function 1 :(失效)
    URL = 'http://www.mktcam.com/gpbiao/cqssc/0/50.html'
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, features='html.parser')
    tags = soup.find_all(name='tr', attrs={'class': 't_tr2'}, recursive=True)

    for item in tags:
        se = list(item.children)[1].get_text()
        qi = list(item.children)[2].get_text()
        print(se, qi)
        SSC_NUMBER.update({se: qi,})

    Function 2 :(失效)
    if not URL:
        URL = 'https://zst.cjcp.com.cn/cjwssc/view/ssc_zst5-ssc-0-3-59.html' # 重庆ssc
        URL = 'https://zst.cjcp.com.cn/cjwssc/view/ssc_zst5-hnwfc-0-3-60.html' # 河内5mins
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, features='html.parser')
    tags = soup.find(name='tbody', attrs={'id': 'pagedata'}, recursive=True)

    tr_tags = tags.find_all(name='tr')

    ssc_number_dict = collections.OrderedDict()

    for item in tr_tags:
        tr_block = item.find_all(name='td')
        se = tr_block[1].get_text()
        qi = tr_block[2].get_text()
        ssc_number_dict.update({se: qi,})
    '''

    check_option = {
        'type': 2,
        'check_hour': 23,
        'start_hours': 17,
        'check_year': 2021,
        'check_month': 7,
        'check_day': 23,
    }

    check_SSC_files(**check_option)
    ssc_number_dict = Read_SSC_Number_From_Files(**check_option)

    return ssc_number_dict

def ssc_number_to_file(url=None):

    ssc_number_dict = get_SSC_Number()

    import os

    dire_path = os.path.join(os.path.abspath('.'),'app01','ssc_number_file')
    file_path = os.path.join(dire_path,'number_file1.txt')

    with open(os.path.abspath(file_path),'w+') as f:
        for qihao, haoma in ssc_number_dict.items():
            write_str = qihao+'-'+haoma
            f.write(write_str+'\n')

    check_option = {
        'type': 1,
        'check_year': 2021,
        'check_month': 7,
        'check_day': 18,
        'check_hour': 23,
        'start_hours': 22,
    }

    temp_1 = ssc_number_dict
    check_SSC_files(**check_option)
    temp = Read_SSC_Number_From_Files(**check_option)
    temp_1.update(temp)

    with open(os.path.abspath(os.path.join(dire_path,'ssc_dict_json.txt')), 'w+') as fp:
        fp.write(json.dumps(temp_1))

def ssc_calculate_ssc(request):
    ''' 预测页面 '''

    ssc_number_to_file()


    SSC_NUMBER = get_SSC_Number()

    print('Done')

    LAST_NUMBER = collections.OrderedDict()
    last_num = None
    for k,v in SSC_NUMBER.items():
        LAST_NUMBER[k] = last_num
        last_num = v

    # ---------- 添加下一期 期号:
    last_no, last_num, LAST_NUMBER = get_last_number(SSC_NUMBER)
    print(last_no, last_num)
    next_seq = find_next_seq(last_no)

    nowtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

    from app01.templatetags import calculate_ssc_number
    calculate_ssc_number.calculate_ssc_number_func_1()
    #print('ssc_calculate_ssc')

    # print('SSC_NUMBER',SSC_NUMBER)
    # print('LAST_NUMBER',LAST_NUMBER)

    print('********************')
    print(nowtime,SSC_NUMBER)
    print(LAST_NUMBER)
    print(next_seq)
    print('********************')

    return render(request,'ssc_calculate.html',{'nowtime':nowtime,
                                             'SSC_NUMBER':SSC_NUMBER,
                                             'LAST_NUMBER':LAST_NUMBER,
                                             'next_seq':next_seq,})



'''  2021.7.19  新增 '''
def get_SSC_An_Hours_Number(type=1,day=None,month=None,year=None,hour=None):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE',
    }

    # https://viet-lotto.com/analy/5fc?day=18&month=7&year=2021&hour=0#
    # https://draw.vietlotto.org/analy.php?day=18&month=7&year=2021&hour=0
    URL_1 = "https://viet-lotto.com/analy/5fc?day={day}&month={month}&year={year}&hour={hour}#".format(day=day,month=month,year=year,hour=hour)
    URL_2 = "https://draw.vietlotto.org/analy.php?day={day}&month={month}&year={year}&hour={hour}".format(day=day,month=month,year=year,hour=hour)

    if type == 1:
        URL = URL_1
    else:
        URL = URL_2

    print('URL :',URL)
    response = requests.get(URL,headers=headers)
    time.sleep(1)

    soup = BeautifulSoup(response.text, features='html.parser')
    tags = soup.find(name='div', attrs={'class': 'list_right_box'}, recursive=True)
    tr_tags = tags.find_all(name='div', attrs={'class': 'item'})

    #print(len(tr_tags))

    if len(tr_tags) != 0:
        ssc_number_dict = collections.OrderedDict()

        for item in tr_tags:
            d_date = item.find_all(name='div', attrs={'class': 'date'})
            b_ball = item.find_all(name='div', attrs={'class': 'ball'})
            se = d_date[0].get_text()
            if '-' in se:
                temp = se.split('-')
                if 1 <= int(temp[1]) < 10:
                    temp[1] = '00{}'.format(temp[1])
                elif  99 >= int(temp[1]) >= 10:
                    temp[1] = '0{}'.format(temp[1])

                se = ''.join(temp)

            qi = "".join(re.findall(">(.*?)<", str(b_ball[0])))
            # print(se, qi)

            ssc_number_dict.update({se: qi,})

        result = collections.OrderedDict(sorted(ssc_number_dict.items()), key=lambda x: x[0])
        temp = result.pop('key', None)
        if temp == None:
            print(' ----------Error----------- None Value')

        return result
    else:
        return None

def get_One_Day_All_Number(days,months,years=2021):

    current_hours = datetime.datetime.now().hour
    ssc_number_dict = collections.OrderedDict()

    for h in range(0,current_hours+1):
        ssc_result = get_SSC_Detail_Number(day=days, month=months, year=years, hour=h)
        print('::: Download For {year}/{month}/{day} {hour}:00-{hours}:00 :::'.format(day=days,month=months,year=years,hour=h,hours=h+1))
        if ssc_result != None:
            ssc_number_dict.update(ssc_result)
        else:
            break

    #ke = collections.OrderedDict(sorted(ssc_number_dict.items()), key=lambda x: x[0])
    result = collections.OrderedDict(sorted(ssc_number_dict.items()), key=lambda x: x[0])
    temp = result.pop('key',None)
    if temp != None:
        print(result)

def check_SSC_files(type=1,check_year=None,check_month=None,check_day=None,check_hour=None,start_hours=0):

    if check_year == None or check_month == None or check_day == None:
        check_year = datetime.datetime.now().year
        check_month = datetime.datetime.now().month
        check_day = datetime.datetime.now().day
        check_hour = datetime.datetime.now().hour
    elif check_year == datetime.datetime.now().year and check_month == datetime.datetime.now().month and check_day ==datetime.datetime.now().day:
        check_hour = datetime.datetime.now().hour
    else:
        check_hour = 23

    print(check_year,check_month,check_day,check_hour)
    dirs_name = '{}-{}-{}'.format(check_year,check_month,check_day)

    if type ==1 :
        path = "I:\\SSC\\type_1\\{}".format(dirs_name)
        print("https://viet-lotto.com/analy/5fc")
    else:
        path = "I:\\SSC\\type_2\\{}".format(dirs_name)
        print("https://draw.vietlotto.org/analy.php?")

    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)

    for h in range(start_hours,check_hour+1):

        file_names = path + "\\{}-{}-{}-{}_00.txt".format(check_year, check_month, check_day, h)
        isExists = os.path.exists(file_names)
        if not isExists or (h == check_hour and  check_day == datetime.datetime.now().day) or os.path.getsize(file_names) <= 220 :
            result_dict = get_SSC_An_Hours_Number(type=type,day=check_day,month=check_month,year=check_year,hour=h)
            with open(file_names,'w+') as f:
                for k,v in result_dict.items():
                    f.write('{}-{}\n'.format(k,v))

        print(
            '::: Download For {year}/{month}/{day} {hour}:00-{hours}:00 :::'.format(day=check_day, month=check_month, year=check_year,
                                                                                    hour=h, hours=h + 1))

def Read_SSC_Number_From_Files(type=1,check_year=None,check_month=None,check_day=None,check_hour=23,start_hours=0):

    if check_year == None or check_month == None or check_day == None:
        check_year = datetime.datetime.now().year
        check_month = datetime.datetime.now().month
        check_day = datetime.datetime.now().day
        check_hour = datetime.datetime.now().hour
    elif check_year == datetime.datetime.now().year and check_month == datetime.datetime.now().month and check_day ==datetime.datetime.now().day:
        check_hour = datetime.datetime.now().hour


    ssc_number_dict = collections.OrderedDict()

    dirs_name = '{}-{}-{}'.format(check_year, check_month, check_day)
    if type == 1:
        path = "I:\\SSC\\type_1\\{}".format(dirs_name)
    else:
        path = "I:\\SSC\\type_2\\{}".format(dirs_name)

    for h in range(start_hours,check_hour+1):
        files_name = "\\{}-{}-{}-{}_00.txt".format(check_year, check_month, check_day, h)
        temp_path = path + files_name
        isExists = os.path.exists(temp_path)
        if isExists:
            with open(temp_path,'r') as f:
                for line in f.readlines():
                    k,v = line.strip().split('-')
                    ssc_number_dict.update({k: v,})

    print(ssc_number_dict)

    return ssc_number_dict
'''  ---------  '''


'''未完成'''
def get_HeNei_SSC(day, month, year, hour):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://www.manycai365.com',
        'Referer': 'http://www.manycai365.com/Issue/history?lottername=HN300',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Mobile Safari/537.36',
    }

    all_ssc_number = collections.OrderedDict()

    current_time = int(time.strftime('%H'))

    for i in range(0,24):
        hour = i
        URL = 'https://draw.vietlotto.org/analy.php?day={}&month={}&year={}&hour={}'.format(day, month, year, hour)

        if i > current_time:
            break

        max_retry = 0
        while max_retry < 3:

            try:
                response = requests.get(URL,headers=headers)

                soup = BeautifulSoup(response.text, features='html.parser')
                tags = soup.find(name='div', attrs={'class':'list_right_box'}, recursive=True)
                tr_tags = tags.find_all(name='div', attrs={'class':'item'})

                for item in tr_tags:

                    d_date = item.find_all(name='div', attrs={'class':'date'})
                    b_ball = item.find_all(name='div', attrs={'class':'ball'})

                    se = d_date[0].get_text()
                    item = se.split('-')
                    if len(item[1]) == 1:
                        b = '00'+item[1]
                        temp = item[0] + b
                        se = temp
                    elif  len(item[1]) == 2:
                        b = '0' + item[1]
                        temp = item[0] + b
                        se = temp
                    else:
                        b = '' + item[1]
                        temp = item[0] + b
                        se = temp


                    qi = b_ball[0].get_text().strip()
                    all_ssc_number.update({se: qi,})

                    # print(all_ssc_number)

                break

            except Exception as e:
                time.sleep(0.5)
                max_retry += 1

    all_ssc_number = collections.OrderedDict(sorted(all_ssc_number.items()), key=lambda x: x[0])


    return all_ssc_number