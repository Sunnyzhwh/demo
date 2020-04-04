from django.db import models

# Create your models here.


class User(models.Model):
    SEX_CHOICE = [
        '男': '男',
        '女': '女'
    ]
    nickname = models.CharField(verbose_name='昵称', unique=True)
    phone = models.CharField(verbose_name='手机号', unique=True)
