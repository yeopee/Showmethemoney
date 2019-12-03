from django.db import models
from django.contrib.auth import settings

# Create your models here.

# userinfo models
# 
# 1. how to use in html page
#       user.info.get.money
#       user.info.get.date

class UserInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='info', on_delete=models.CASCADE)

    money = models.IntegerField(default=1000)
    date = models.DateTimeField(auto_now_add=True)