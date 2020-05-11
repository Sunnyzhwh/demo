import os
import sys
import random

import django

# 设置环境


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BACKEND_DIR = os.path.join(BASE_DIR, 'backend')

sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tantan.settings")
django.setup()

from api.models import User
from VIP.models import Permission, Vip, VipPermRelation

last_names = (
    '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨'
    '朱秦尤许何吕施张孔曹严华金魏陶姜'
    '戚谢邹喻柏水窦章云苏潘葛奚范彭郎'
    '鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
    '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常'
    '乐于时傅皮卞齐康伍余元卜顾孟平黄'
)

first_names = {
    '男': [
        '致远', '建国', '雨泽', '叶磊', '晟睿',
        '天佑', '文豪', '士林', '向南', '远航',
        '洪涛', '宇轩', '文轩', '圣杰', '思聪',
        '建军', '八一', '凯旋', '起灵', '邵琦',
        '国涛', '成才', '经凯', '树茂', '云龙',
    ],
    '女': [
        '爱玲', '玉婷', '宇佳', '梦洁', '意涵',
        '美玲', '梦露', '菱纱', '雅韵', '碧莲',
        '媚娘', '馨启', '思涵', '文娟', '文静',
        '宁静', '心凌', '韶涵', '静茹', '圆圆',
        '静雯', '梓涵', '妃丽', '秀丽', '雅芝',
    ]
}


def random_name():
    last_name = random.choice(last_names)
    random_sex = random.choice(['男', '女'])
    first_name = random.choice(first_names[random_sex])
    return ''.join([last_name, first_name]), random_sex


def create_robots(n):
    for i in range(n):
        name, sex = random_name()
        try:
            u = User.objects.create(
                phone='%s' % random.randrange(21000000000, 21900000000),
                nickname=name,
                sex=sex,
                birth_year=random.randint(1980, 2000),
                birth_month=random.randint(1, 12),
                birth_day=random.randint(1, 28),
                location=random.choice(['北京', '上海', '天津', '深圳', '广州', '武汉', '南京', '沈阳'])
            )
            p = u.profile
            print('created %s %s' % (name, sex))
            print(p.id)
        except django.db.utils.IntegrityError:
            pass


def init_permission():
    """创建权限模型"""
    permission_names = [
        'vipflag',
        'superlike',
        'rewind',
        'anylocation',
        'unlimit_like',
    ]
    for name in permission_names:
        Permission.objects.create(name=name)


def init_vip():
    for i in range(4):
        Vip.objects.create(
            name='会员-%d' % i,
            level=i,
            price=i * 5
        )


def create_vip_perm_relations():
    """创建VIP和权限的关系"""
    # 获取VIP
    vip1 = Vip.objects.get(level=1)
    vip2 = Vip.objects.get(level=2)
    vip3 = Vip.objects.get(level=3)
    # 获取权限
    vipflag = Permission.objects.get(name='vipflag')
    superlike = Permission.objects.get(name='superlike')
    rewind = Permission.objects.get(name='rewind')
    anylocation = Permission.objects.get(name='anylocation')
    unlimit_like = Permission.objects.get(name='unlimit_like')
    # 给VIP1分配权限
    VipPermRelation.objects.create(vip_id=vip1.id, perm_id=vipflag.id)
    VipPermRelation.objects.create(vip_id=vip1.id, perm_id=superlike.id)
    # 给VIP2分配权限
    VipPermRelation.objects.create(vip_id=vip2.id, perm_id=vipflag.id)
    VipPermRelation.objects.create(vip_id=vip2.id, perm_id=rewind.id)
    # 给VIP3分配权限
    VipPermRelation.objects.create(vip_id=vip3.id,
                                   perm_id=vipflag.id)
    VipPermRelation.objects.create(vip_id=vip3.id,
                                   perm_id=superlike.id)
    VipPermRelation.objects.create(vip_id=vip3.id,
                                   perm_id=rewind.id)
    VipPermRelation.objects.create(vip_id=vip3.id,
                                   perm_id=anylocation.id)
    VipPermRelation.objects.create(vip_id=vip3.id,
                                   perm_id=unlimit_like.id)


if __name__ == '__main__':
    # init_permission()
    # init_vip()
    # create_vip_perm_relations()
    create_robots(1000)
