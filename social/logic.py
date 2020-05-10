import datetime

from api.models import User
from social.models import Swiped, Friend


def get_rcmd_users(user):
    """获取推荐用户"""
    sex = user.profile.dating_sex
    location = user.profile.dating_city
    min_age = user.profile.min_dating_age
    max_age = user.profile.max_dating_age

    current_year = datetime.date.today().year
    min_year = current_year - max_age
    max_year = current_year - min_age

    users = User.objects.filter(sex=sex, location=location,
                                birth_year__gte=min_year,
                                birth_year__lte=max_year)
    return users


def like(user, sid):
    # 标记一个滑动记录
    Swiped.mark(user.id, sid, 'like')
    # 检查被滑动的用户是否喜欢过自己
    if Swiped.is_liked(sid, user.id):
        Friend.be_friends(user.id, sid)
        return True
    else:
        return False


def superlike(user, sid):
    # 标记一个滑动记录
    Swiped.mark(user.id, sid, 'superlike')
    # 检查被滑动的用户是否喜欢过自己
    if Swiped.is_liked(sid, user.id):
        Friend.be_friends(user.id, sid)
        return True
    else:
        return False


def dislike(user, sid):
    Swiped.mark(user.id, sid, 'dislike')


def rewind(user, sid):
    """反悔"""
    try:
        # 取消滑动记录
        Swiped.objects.get(uid=user.id, sid=sid).delete()
    except Swiped.DoesNotExist:
        pass

    # 撤销好友关系
    Friend.break_off(user.id, sid)
