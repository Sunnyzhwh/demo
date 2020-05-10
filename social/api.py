from rest_framework.views import APIView

from api.models import User
from lib.http import render_json

from social.logic import get_rcmd_users


class GetRecommendUsers(APIView):
    """获取推荐列表"""

    @staticmethod
    def get(request):
        payload = request.user
        user = User.objects.get(id=payload['id'])
        group_num = int(request.GET.get('group_num', 0))
        start = group_num * 5
        end = start + 5
        users = get_rcmd_users(user)[start:end]
        result = [user.to_dict for user in users]
        return render_json(result)





def like(request):
    """喜欢"""
    return render_json()


def superlike(request):
    """超级喜欢"""
    return render_json()


def dislike(request):
    """不喜欢"""
    return render_json()


def rewind(request):
    """反悔"""
    return render_json()
