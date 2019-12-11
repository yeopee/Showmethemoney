
from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.decorators import login_required

from . import parse_lotto
import json

from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm
from accounts.models import CustomUser

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def lotto(request):
    if request.user.money < 1000:
        return redirect('/lotto/#GasStation')

    user = CustomUser.objects.get(id=request.user.id)
    user.money -= 1000
    user.save()

    context = {
        'numbers' : range(1,46)
    }

    return render(request, 'lotto.html', context)

@login_required
def request_lotto_number_sum(request):
    lotto_data = parse_lotto.get_all_lotto_data()
    sum_lotto_data = parse_lotto.get_lotto_number_sum(lotto_data)

    context = {
        'sum_lotto_data' : sum_lotto_data
    }

    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def request_lotto_number_each_win_count(request):
    lotto_data = parse_lotto.get_all_lotto_data()
    lotto_number_each_win_count = parse_lotto.get_lotto_number_each_win_count(lotto_data)

    context = {
        'lotto_number_each_win_count' : lotto_number_each_win_count
    }

    return HttpResponse(json.dumps(context), content_type='application/json')

@login_required
def request_lotto_number_duration_win_count(request):
    lotto_data = parse_lotto.get_all_lotto_data()
    lotto_number_duration_win_count = parse_lotto.get_lotto_number_duration_win_count(lotto_data)

    context = {
        'lotto_number_duration_win_count' : lotto_number_duration_win_count
    }

    return HttpResponse(json.dumps(context), content_type='application/json')
    
# lotto_data_test
#       This function is for testing lotto_data

def lotto_data_test(request):
    lotto_data = parse_lotto.get_all_lotto_data()

    lotto_number_sum = parse_lotto.get_lotto_number_sum(lotto_data)

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
        'result': result
    }
    
    return HttpResponse(json.dumps(context),content_type="application/json")

def lotto_data_highchaet(request):
    return render(request,'test/highchart.html')

def lotto_data_test2(request):
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

   

