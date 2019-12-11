"""show_me_the_money URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views as lotto_views

app_name = 'lotto'

urlpatterns = [
    path('', lotto_views.index, name='index'),
    path('lotto/', lotto_views.lotto, name='lotto'),
    path('request_lotto_number_sum/', lotto_views.request_lotto_number_sum, name='request_lotto_number_sum'),
    path('request_lotto_number_each_win_count/', lotto_views.request_lotto_number_each_win_count, name='request_lotto_number_each_win_count'),
    path('request_lotto_number_duration_win_count/', lotto_views.request_lotto_number_duration_win_count, name='request_lotto_number_duration_win_count'),
    path('request_lotto_number_year_win_count/', lotto_views.request_lotto_number_year_win_count, name='request_lotto_number_year_win_count')
]
