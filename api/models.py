import datetime

from django.db import models
from django.utils.functional import cached_property

from lib.orm import ModelMixin


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

    # 计算年龄,缓存属性，属于Django里面的装饰器
    @cached_property
    def age(self):
        now = datetime.date.today()
        delta = (now.month, now.day) < (self.birth_month, self.birth_day)
        result_age = now.year - self.birth_year - delta
        return result_age

    @property
    def profile(self):
        """用户配置关联,作用类似于外键"""
        # 给self添加属性到dict里面,是对象的属性字典
        # if '_profile' not in self.__dict__:
        #     _profile, _ = Profile.objects.get_or_create(id=self.id)
        #     self._profile = _profile
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    def __str__(self):
        return self.nickname

    @property
    def to_dict(self):
        dicts = {
            'id': self.id,
            'phone': self.phone,
            'sex': self.sex,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'location': self.location,
            'age': self.age,
            'birth_year': self.birth_year,
            'birth_month': self.birth_month,
            'birth_day': self.birth_day,
            'profile': [self.profile.to_dict()],
        }
        return dicts


class Profile(models.Model, ModelMixin):
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
        return str(self.id)
