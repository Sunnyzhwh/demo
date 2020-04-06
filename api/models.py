import datetime

from django.db import models


# Create your models here.


class User(models.Model):
    """用户数据模型"""
    SEX_CHOICE = (
        ('男', '男'),
        ('女', '女'),
    )
    phone = models.CharField(verbose_name='手机号', unique=True, max_length=16, null=True)
    nickname = models.CharField(verbose_name='昵称', unique=True, max_length=32, null=True)
    pwd = models.CharField(verbose_name='密码', max_length=64)
    token = models.CharField(
        max_length=64, verbose_name='授权令牌', blank=True, null=True)
    sex = models.CharField(max_length=8, choices=SEX_CHOICE, default='男')
    avatar = models.CharField(max_length=256, null=True)
    location = models.CharField(max_length=32, default='北京')

    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)

    # 计算年龄
    @property
    def age(self):
        now = datetime.date.today()
        delta = (now.month, now.day) < (self.birth_month, self.birth_day)
        result_age = now.year - self.birth_year - delta
        return result_age

    def __str__(self):
        return self.nickname


class Profile(models.Model):
    """用户配置模型"""
    SEX_CHOICE = (
        ('男', '男'),
        ('女', '女'),
    )
    dating_sex = models.CharField(default='女', max_length=8, choices=SEX_CHOICE)
    dating_city = models.CharField(default='北京', max_length=32, verbose_name='目标城市')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小约会年龄')
    max_dating_age = models.IntegerField(default=49, verbose_name='最大约会年龄')
    min_distance = models.IntegerField(default=1, verbose_name='最小约会距离')
    max_distance = models.IntegerField(default=10, verbose_name='最大约会距离')
    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_match = models.BooleanField(default=True, verbose_name='是否好友可见')
    auto_play = models.BooleanField(default=True, verbose_name='是否自动播放')

    def __str__(self):
        return self.id
