from django.db import models


# Create your models here.
class Swiped(models.Model):
    STATUS = (
        ('superlike', '超级喜欢'),
        ('like', '喜欢'),
        ('dislike', '不喜欢'),
    )
    uid = models.IntegerField(verbose_name='滑动者的UID')
    sid = models.IntegerField(verbose_name='被滑动者的UID')
    status = models.CharField(max_length=10, choices=STATUS)
    time = models.DateTimeField(auto_now_add=True)


class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()
