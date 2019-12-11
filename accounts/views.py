from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser

import json

# Create your views here.

def accounts_test(request):
    return render(request, 'test/login_test.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('lotto:index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            return redirect(request.POST.get('next') or 'lotto:index')

    return render(request, 'signin.html')

def signout(request):
    if request.user.is_authenticated:
        auth_logout(request)

        return redirect('lotto:index')

    return redirect('accounts:login')

def signup(request):
    if request.user.is_authenticated:
        return redirect('lotto:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            return redirect('lotto:index')

    return render(request, 'signup.html')

@login_required
def chargeMoneyWithoutAd(request):
    if request.method == 'POST' and request.is_ajax:
        user = CustomUser.objects.get(id=request.user.id)
        user.money += 1
        user.save()

        money = user.money

        context = {
            'money' : money
        }

        return HttpResponse(json.dumps(context), content_type='application/json')
    
    return HttpResponse(status=403)

@login_required
def chargeMoneyWithAd(request):
    if request.method == 'POST' and request.is_ajax:
        user = CustomUser.objects.get(id=request.user.id)
        user.money += 500
        user.save()

        money = user.money

        context = {
            'money' : money
        }

        return HttpResponse(json.dumps(context), content_type='application/json')
    
    return HttpResponse(status=403)