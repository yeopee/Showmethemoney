from django.shortcuts import render,HttpResponse
from . import parse_lotto
import json
# Create your views here.

def index(request):
    return render(request, 'index.html')

# lotto_data_test
#       This function is for testing lotto_data

def lotto_data_test(request):
    lotto_data = parse_lotto.get_lotto_data(parse_lotto.get_lotto_cnt())
    
    lotto_number_sum = parse_lotto.get_lotto_number_sum(lotto_data)
    lotto_number_win_count = parse_lotto.get_lotto_number_win_count(lotto_data)
    lotto_number_each_win_count = parse_lotto.get_lotto_number_each_win_count(lotto_data)

    context = {
        'lotto_number_sum' : lotto_number_sum,
        'lotto_number_win_count' : lotto_number_win_count,
        'lotto_number_each_win_count' : lotto_number_each_win_count
    }

    result =[]

    for tmp in range(1,46):
        a = lotto_number_sum[tmp]

        one = {
            'name':tmp,
            'y':a,
            'drilldown':tmp
        }

        result.append(one)
    
    context={
        'result':result
    }
    
    return HttpResponse(json.dumps(context),content_type="application/json")

def lotto_data_highchaet(request):

    return render(request,'test/highchart.html')