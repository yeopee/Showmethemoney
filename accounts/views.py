from django.shortcuts import render, redirect

# Create your views here.

def signin(request):
    if request.method == 'POST':
        return redirect('accounts:signin')
    else:
        return render(request, 'signin.html')