from django.urls import path
from . import views as lottogame_views

app_name = 'lottogame'

urlpatterns = [
    path('',lottogame_views.index, name='game'),
    path('result/',lottogame_views.result,name='result')
]