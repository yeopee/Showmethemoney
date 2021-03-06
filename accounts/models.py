from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    money = models.IntegerField(default=1000)

    def get_username(self):
        return self.username.split('@')[0]