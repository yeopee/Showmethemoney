from django.shortcuts import render
from . import parse_lotto

# Create your views here.

def index(request):
    return render(request, 'index.html')

# lotto_data_test
#       This function is for testing lotto_data

def lotto_data_test(request):
    lotto_data = parse_lotto.get_all_lotto_data()

    lotto_number_sum = parse_lotto.get_lotto_number_sum(lotto_data)
    lotto_number_win_count = parse_lotto.get_lotto_number_win_count(lotto_data)
    lotto_number_each_win_count = parse_lotto.get_lotto_number_each_win_count(lotto_data)

    context = {
        'lotto_data' : lotto_data,
        'lotto_number_sum' : lotto_number_sum,
        'lotto_number_win_count' : lotto_number_win_count,
        'lotto_number_each_win_count' : lotto_number_each_win_count
    }

    return render(request, 'test/lotto_data.html', context)