from bs4 import BeautifulSoup
import requests
import collections

from .models import Lotto, WinningData

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

# get_lotto_number_data function
#
# 1. request_lotto_data
# 2. parse_lotto_data_from_page
# 3. save_lotto_data_to_storage
# 4. parse_lotto_data_from_storage
# 5. lotto_data_is_saved_in_storage
#
# 6. get_one_lotto_number_data
# 7. get_all_lotto_number_data
# 8. get_lotto_number_data
# 
# This functions can get total lotto datas from web site or from storage
# 
# Data Format
# 
# lotto_data = {
#   lotto_count : {
#       'date' : date,
#       'numbers' : [first_num, second_num, ... , bonus_num ]
#   }
# }

def request_lotto_data(url, cnt, params):
    response = requests.post(url, params=params)

    return response

def save_lotto_data_to_storage(title, date, numbers):
    if Lotto.objects.filter(count=int(title)).count() == 0:
        lotto = Lotto()

        lotto.count = int(title)
        lotto.date = date

        lotto.nums_1 = numbers[0]
        lotto.nums_2 = numbers[1]
        lotto.nums_3 = numbers[2]
        lotto.nums_4 = numbers[3]
        lotto.nums_5 = numbers[4]
        lotto.nums_6 = numbers[5]
        lotto.nums_bonus = numbers[6]

        lotto.save()

def parse_lotto_data_from_page(response, lotto_data):
    html = BeautifulSoup(response.text, 'html.parser')
    lotto_list = html.select('li')

    for lotto in lotto_list:
        title = lotto.select('span')[0].text[0:-1]
        date = lotto.select('span')[1].text
        item = lotto.select_one('a.cur_wnr_item')

        numbers = []

        for lotto_num in item.select('img.wball'):
            num_with_png = lotto_num['src'].split('/')[5]
            num = num_with_png.split('.')[0]

            numbers.append(int(num))

        lotto_data[int(title)] = {
            'date' : date,
            'numbers' : numbers
        }
        
        save_lotto_data_to_storage(title, date, numbers)

def parse_lotto_data_from_storage(count, lotto_data):
    lotto = Lotto.objects.get(count=count)
    
    count = lotto.get_count()
    date = lotto.get_date()
    numbers = lotto.get_number_array()

    lotto_data[count] = {
        'date' : date,
        'numbers' : numbers
    }

def lotto_data_is_saved_in_storage(count):
    lotto_data = Lotto.objects.filter(count=count)

    if lotto_data.count() == 1:
        return True
    else:
        return False

def get_one_lotto_number_data(cnt, count, lotto_data):
    if lotto_data_is_saved_in_storage(count):
        print(f'get_lotto_data : {count} - from storage')

        parse_lotto_data_from_storage(count, lotto_data)

    else:
        print(f'get_lotto_data : {count} - from web page')

        url = 'http://www.lotto.co.kr/lotto_info/list_ajax'

        params = {
            'category' : 'AC01',
            'total' : cnt,
            'startPos' : cnt - count,
            'endPos' : cnt - count + 1,
            'pageSize' : 1,
            'code_type_id' : 2
        }

        response = request_lotto_data(url, cnt, params)
        parse_lotto_data_from_page(response, lotto_data)

def get_all_lotto_number_data():
    lotto_data = {}
    cnt = get_lotto_cnt()

    for count in range(1, cnt + 1):
        get_one_lotto_number_data(cnt, count, lotto_data)

    return lotto_data

def get_lotto_number_data(count):
    lotto_data = {}
    cnt = get_lotto_cnt()

    if count > cnt:
        print(f'{count} request is wrong')

        return lotto_data
    else:
        get_one_lotto_number_data(cnt, count, lotto_data)
    
        return lotto_data

# get_lotto_winning_data function
#
# 1. parse_lotto_winning_data_from_page
# 2. save_lotto_winning_data_to_storage
# 3. parse_lotto_winning_data_from_storage
# 4. lotto_winning_data_is_saved_in_storage
#
# 5. get_one_lotto_winning_data
# 6. get_all_lotto_winning_data
# 7. get_lotto_winning_data
#
# This functions can get total lotto winning datas from web site or from storage
# 
# Data Format
#
# lotto_winning_data = {
#   lotto_count : {
#       1 : {
#           'total_money' : total_money,
#           'winner' : winner,
#           'each_money' : each_money
#       },
#       
#       2 : {
#           ...
#       },
#       ...
#       
#       5 : {
#           'total_money' : total_money,
#           'winner' : winner,
#           'each_money' : each_money
#       }
#   }
# }

def save_lotto_winning_data_to_storage(title, rank, winning_data):
    if WinningData.objects.filter(count=int(title), rank=rank).count() == 0:
        new_winning_data = WinningData()
        
        new_winning_data.count = int(title)
        new_winning_data.rank = rank
        new_winning_data.total_money = winning_data['total_money']
        new_winning_data.winner = winning_data['winner']
        new_winning_data.each_money = winning_data['each_money']

        new_winning_data.lotto_id = Lotto.objects.get(count=int(title)).id

        new_winning_data.save()

def parse_lotto_winning_data_from_page(response, lotto_winning_data):
    html = BeautifulSoup(response.text, 'html.parser')

    title = html.select_one('strong').text[1:-1]
    lotto_list = html.select('table tbody tr')

    lotto_winning_data[int(title)] = {}

    for lotto in lotto_list:
        winning_data = {}
        
        data = lotto.select('td')

        rank = int(data[0].text[0:-1])
        total_money = data[1].text
        winner = data[2].text
        each_money = data[3].text

        winning_data['total_money'] = total_money
        winning_data['winner'] = winner
        winning_data['each_money'] = each_money

        lotto_winning_data[int(title)][rank] = winning_data
        save_lotto_winning_data_to_storage(title, rank, winning_data)

def parse_lotto_winning_data_from_storage(cnt, lotto_winning_data):
    lotto = Lotto.objects.get(count=cnt)
    lotto_winning_data[lotto.count] = lotto.get_winning_data_dict()

def lotto_winning_data_is_saved_in_storage(cnt):
    winning_data = WinningData.objects.filter(count=cnt)

    if winning_data.count() == 5:
        return True
    else:
        return False

def get_one_lotto_winning_data(count, lotto_winning_data):
    if lotto_winning_data_is_saved_in_storage(count):
        print(f'get_lotto_winning_data : {count} - parse from storage')

        parse_lotto_winning_data_from_storage(count, lotto_winning_data)

    else:
        print(f'get_lotto_winning_data : {count} - parse from web page')

        url = 'http://www.lotto.co.kr/lotto_info/getHTML'

        params = {
            'grwno' : count,
            'category' : 'AC01'
        }

        response = request_lotto_data(url, count, params)
        parse_lotto_winning_data_from_page(response, lotto_winning_data)

def get_all_lotto_winning_data():
    lotto_winning_data = {}

    cnt = get_lotto_cnt()

    for count in range(1, cnt + 1):
        get_one_lotto_winning_data(count, lotto_winning_data)

    return lotto_winning_data

def get_lotto_winning_data(count):
    lotto_winning_data = {}
    cnt = get_lotto_cnt()

    if count > cnt:
        print(f'{count} request is wrong')
    else:
        get_one_lotto_winning_data(count, lotto_winning_data)

    return lotto_winning_data

# get_lotto_data functions
# 
# 1. get_all_lotto_data
# 2. get_lotto_data
# 
# Data Format
# 
# lotto_data = {
#   count : {
#       'date' : date,
#       'numbers' : numbers,
#       'winning_data' : {
#           1 : {
#               'total_money' : total_money,
#               'winner' : winner,
#               'each_money' : each_money
#           },
#
#           2 : {
#               ...
#           },
#
#           ...
#
#           5 : {
#               ...
#           }
#       }
#   }
# }

def get_all_lotto_data():
    lotto_data = {}

    lotto_number_data = get_all_lotto_number_data()
    lotto_winning_data = get_all_lotto_winning_data()

    for count in lotto_number_data.keys():
        lotto_data[count] = {
            'date' : lotto_number_data[count]['date'],
            'numbers' : lotto_number_data[count]['numbers'],
            'winning_data' : lotto_winning_data[count]
        }

    return lotto_data

def get_lotto_data(count):
    lotto_data = {}

    lotto_number_data = get_lotto_number_data(count)
    lotto_winning_data = get_lotto_winning_data(count)

    if len(lotto_number_data) == 0:
        return lotto_data
    else:
        lotto_data[count] = {
            'date' : lotto_number_data[count]['date'],
            'numbers' : lotto_number_data[count]['numbers'],
            'winning_data' : lotto_winning_data[count]
        }

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
        for number in numbers['numbers']:
            if lotto_number_sum.get(number) == None:
                lotto_number_sum[number] = 1
            else:
                lotto_number_sum[number] = lotto_number_sum[number] + 1
    
    return collections.OrderedDict(sorted(lotto_number_sum.items()))

def get_lotto_number_win_count(total_numbers):
    lotto_number_win = {}

    for count, numbers in total_numbers.items():
        for number in numbers['numbers']:
            if lotto_number_win.get(number) == None:
                lotto_number_win[number] = []
                lotto_number_win[number].append(count)
            else:
                lotto_number_win[number].append(count)
    
    return collections.OrderedDict(sorted(lotto_number_win.items()))

def get_lotto_number_each_win_count(total_numbers):
    lotto_number_each_win = {}

    for count, numbers in total_numbers.items():
        for number in numbers['numbers']:
            if lotto_number_each_win.get(number) == None:
                lotto_number_each_win[number] = {}
                
            lotto_number_each_win[number][count] = 1
        
        for number in range(1, 46):
            if lotto_number_each_win.get(number) == None:
                lotto_number_each_win[number] = {}

            if lotto_number_each_win[number].get(count) == None:
                lotto_number_each_win[number][count] = 0
    
    return collections.OrderedDict(sorted(lotto_number_each_win.items()))