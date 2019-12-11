from django.shortcuts import render,redirect,HttpResponseRedirect,resolve_url
from django.http import HttpResponse
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    #urlstr = 'lotto/#GasStation'

    user = CustomUser.objects.get(id=request.user.id)
    
    if user.money < 500:
        return redirect('/lotto/#GasStation')
        #포인트 채우는 url로 보내줍시다 .
    return render(request,'game.html')

def result(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=403)

    user = CustomUser.objects.get(id=request.user.id)
  
    if request.method == 'POST' and request.is_ajax():
        cnt = int(request.POST['cnt'])
    
        if cnt == 0:
            user.money -= 500
            user.save()
            return HttpResponse(status=204)
        elif cnt == 1:
            user.money -= 500
            user.money += 100
            user.save()
            return HttpResponse(status=204)
        elif cnt == 2:
            user.money -= 500
            user.money += 300
            user.save()
            return HttpResponse(status=204)
        elif cnt == 3:
            user.money -= 500
            user.money += 500
            user.save()
            return HttpResponse(status=204)
        elif cnt == 4:
            user.money -= 500
            user.money += 800
            user.save()
            return HttpResponse(status=204)
        elif cnt == 5:
            user.money -= 500
            user.money += 1000
            user.save()
            return HttpResponse(status=204)
        elif cnt == 6:
            user.money -= 500
            user.money += 2000
            user.save()
            return HttpResponse(status=204)



    return HttpResponse(status=204)