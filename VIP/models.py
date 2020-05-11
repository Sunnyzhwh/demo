from django.db import models


# Create your models here.
class Vip(models.Model):
    name = models.CharField(max_length=32, unique=True)
    level = models.IntegerField()
    price = models.FloatField()

    def vip_perm(self):
        """当前VIP具有的所有权限"""
        relations = VipPermRelation.objects.filter(vip_id=self.id)
        perm_id_list = [r.perm_id for r in relations]
        return Permission.objects.filter(id__in=perm_id_list)

    def has_perm(self, perm_name):
        """检查是否具有某种权限"""
        perm = Permission.objects.get(name=perm_name)
        return VipPermRelation.objects.filter(vip_id=self.id, perm_id=perm.id).exists()


class Permission(models.Model):
    """权限表
        会员身份
        超级喜欢
        反悔功能
        任意更改定位
        无限喜欢次数
    """
    name = models.CharField(max_length=32, unique=True)


class VipPermRelation(models.Model):
    """
    会员-权限 关系表
    VIP1
        身份标示
        超级喜欢
    VIP2
        身份标示
        反悔功能
        无限喜欢次数
    VIP3
        身份标示
        超级喜欢
        反悔功能
        任意更改定位
        无限喜欢次数
    """
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()
