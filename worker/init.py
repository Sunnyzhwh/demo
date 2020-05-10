
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


for i in range(1000):
    name, sex = random_name()
    try:
        User.objects.create(
            phone='%s' % random.randrange(21000000000, 21900000000),
            nickname=name,
            sex=sex,
            birth_year=random.randint(1980, 2000),
            birth_month=random.randint(1, 12),
            birth_day=random.randint(1, 28),
            location=random.choice(['北京', '上海', '天津', '深圳', '广州', '武汉', '南京', '沈阳'])
        )
        print('created %s %s' % (name, sex))
    except django.db.utils.IntegrityError:
        pass
