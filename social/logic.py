import datetime

from api.models import User


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
