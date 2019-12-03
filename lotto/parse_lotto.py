from bs4 import BeautifulSoup
import requests
import collections

# get_lotto_cnt function
#
# 1. request_lotto_cnt
# 2. get_lotto_cnt
# 
# This functions can get total lotto count from web site
 
def request_lotto_cnt(url):
    data = {
        'category' : 'AC01'
    }

    response = requests.post(url, data=data)

    return response

def get_lotto_cnt():
    url = 'http://www.lotto.co.kr/lotto_info/list_cnt_ajax'

    response = request_lotto_cnt(url)
    cnt_json = response.json()

    return int(cnt_json['count'])

# get_lotto_data function
#
# 1. request_lotto_data
# 2. parse_lotto_data
# 3. get_lotto_data
#
# This functions can get total lotto datas from web site
# 
# Data Format
#
# lotto_numbers = {
#   lotto_count : [first_num, second_num, ... , seventh_num ],
#   lotto_count : [first_num, second_num, ... , seventh_num ],
#   ...
# }

def request_lotto_data(url, cnt):
    params = {
        'category' : 'AC01',
        'total' : cnt
    }

    response = requests.post(url, params=params)

    return response

def parse_lotto_data(response):
    html = BeautifulSoup(response.text, 'html.parser')
    lotto_list = html.select('li')

    lotto_numbers = {}

    for lotto in lotto_list:
        title = lotto.select_one('span').text[0:-1]
        item = lotto.select_one('a.cur_wnr_item')

        numbers = []

        for lotto_num in item.select('img.wball'):
            num_with_png = lotto_num['src'].split('/')[5]
            num = num_with_png.split('.')[0]

            numbers.append(int(num))
        
        lotto_numbers[int(title)] = numbers
    
    return lotto_numbers

def get_lotto_data(cnt):
    url = 'http://www.lotto.co.kr/lotto_info/list_ajax'

    response = request_lotto_data(url, cnt)
    lotto_data = parse_lotto_data(response)

    return lotto_data

# lotto data rework functions
#
# 1. get_lotto_number_sum
#       This function can get total sum of each lotto number
#
# 2. get_lotto_number_win_count
#       This function can get win count of each lotto number
#
# 3. get_lotto_number_each_win_count
#       This function ca nget each win count of each lotto number

def get_lotto_number_sum(total_numbers):
    lotto_number_sum = {}

    for numbers in total_numbers.values():
        for number in numbers:
            if lotto_number_sum.get(number) == None:
                lotto_number_sum[number] = 1
            else:
                lotto_number_sum[number] = lotto_number_sum[number] + 1
    
    return collections.OrderedDict(sorted(lotto_number_sum.items()))

def get_lotto_number_win_count(total_numbers):
    lotto_number_win = {}

    for count, numbers in total_numbers.items():
        for number in numbers:
            if lotto_number_win.get(number) == None:
                lotto_number_win[number] = []
                lotto_number_win[number].append(count)
            else:
                lotto_number_win[number].append(count)
    
    return collections.OrderedDict(sorted(lotto_number_win.items()))

def get_lotto_number_each_win_count(total_numbers):
    lotto_number_each_win = {}

    for count, numbers in total_numbers.items():
        for number in numbers:
            if lotto_number_each_win.get(number) == None:
                lotto_number_each_win[number] = {}
                
            lotto_number_each_win[number][count] = 1
        
        for number in range(1, 46):
            if lotto_number_each_win.get(number) == None:
                lotto_number_each_win[number] = {}

            if lotto_number_each_win[number].get(count) == None:
                lotto_number_each_win[number][count] = 0
    
    return collections.OrderedDict(sorted(lotto_number_each_win.items()))