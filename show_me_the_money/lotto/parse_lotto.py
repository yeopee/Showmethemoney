from bs4 import BeautifulSoup
import requests

def request_lotto_data(url):
    params = {
        'category' : 'AC01',
        'startPos' : 0,
        'endPos' : 10,
        'total' : 884,
        'page' : 1,
        'code_type_id' : 2
    }

    response = requests.post(url, params=params)

    return response

def parse_lotto_data(response):
    html = BeautifulSoup(response.text, 'html.parser')
    lotto_list = html.select('li')

    total_numbers = {}

    for lotto in lotto_list:
        title = lotto.select_one('span').text[0:-1]
        item = lotto.select_one('a.cur_wnr_item')

        numbers = []

        for lotto_num in item.select('img.wball'):
            num_with_png = lotto_num['src'].split('/')[5]
            num = num_with_png.split('.')[0]

            numbers.append(num)
        
        total_numbers[title] = numbers
    
    return total_numbers

def sum_lotto_data(total_numbers):
    sum_each_numbers = {}

    for numbers in total_numbers.values():
        for number in numbers:
            if sum_each_numbers.get(number) == None:
                sum_each_numbers[number] = 1
            else:
                sum_each_numbers[number] = sum_each_numbers[number] + 1
    
    return sum_each_numbers

def each_lotto_data(total_numbers):
    each_numbers = {}

    for count, numbers in total_numbers.items():
        for number in numbers:
            if each_numbers.get(number) == None:
                each_numbers[number] = []
                each_numbers[number].append(count)
            else:
                each_numbers[number].append(count)
    
    return each_numbers

def each_count_lotto_data(total_numbers):
    each_count_numbers = {}

    for count, numbers in total_numbers.items():
        for number in numbers:
            if each_count_numbers.get(number) == None:
                each_count_numbers[number] = {}
                
            each_count_numbers[number][count] = 1
        
        for number in range(1, 46):
            if each_count_numbers.get(str(number)) == None:
                each_count_numbers[str(number)] = {}

            if each_count_numbers[str(number)].get(count) == None:
                each_count_numbers[str(number)][count] = 0
    
    return each_count_numbers

def get_each_numbers_win_counts():
    url = 'http://www.lotto.co.kr/lotto_info/list_ajax'
    response = request_lotto_data(url)

    total_numbers = parse_lotto_data(response)
    # sum_each_numbers = sum_lotto_data(total_numbers)
    # each_numbers = each_lotto_data(total_numbers)
    each_count_numbers = each_count_lotto_data(total_numbers)

    return each_count_numbers