from django.urls import path
from . import views as lottogame_views

app_name = 'lottogame'

urlpatterns = [
    path('',lottogame_views.index, name='game'),
   
]