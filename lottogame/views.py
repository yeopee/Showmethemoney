from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.

def index(request):
    
    return render(request,'game.html')



def result(request):
    if request.method == 'POST' and request.is_ajax():
        cnt = request.POST['cnt']
        




    return HttpResponse(status=204)