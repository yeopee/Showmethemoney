from django.shortcuts import render, redirect

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import UserInfo

# Create your views here.

def accounts_test(request):
    return render(request, 'test/login_test.html')

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            return redirect('accounts:test')
        
        else:
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')

def signout(request):
    if request.method == 'POST':
        auth_logout(request)

        return redirect('accounts:signin')

    else:
        return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            user_info = UserInfo()
            user_info.user = user
            user_info.save()

            user.info = user_info
            user.save()

            auth_login(request, user)

            return redirect('accounts:test')

        else:
            return render(request, 'signup.html')
    
    else:
        return render(request, 'signup.html')