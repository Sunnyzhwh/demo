from rest_framework.views import APIView

from api.models import User
from lib.http import render_json

from social.logic import get_rcmd_users, like, superlike, dislike, rewind
from social.models import Friend


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


class Like(APIView):
    """喜欢"""

    @staticmethod
    def post(request):
        payload = request.user
        user = User.objects.get(id=payload['id'])
        sid = request.POST.get('sid')
        is_matched = like(user, sid)
        return render_json({'is_matched': is_matched})


class SuperLike(APIView):
    """超级喜欢"""

    @staticmethod
    def post(request):
        payload = request.user
        user = User.objects.get(id=payload['id'])
        sid = request.POST.get('sid')
        is_matched = superlike(user, sid)
        return render_json({'is_matched': is_matched})


class Dislike(APIView):
    """不喜欢"""

    @staticmethod
    def post(request):
        payload = request.user
        user = User.objects.get(id=payload['id'])
        sid = request.POST.get('sid')
        dislike(user, sid)
        return render_json(None)


class Rewind(APIView):
    """反悔"""

    @staticmethod
    def post(request):
        payload = request.user
        user = User.objects.get(id=payload['id'])
        sid = request.POST.get('sid')
        rewind(user, sid)
        return render_json(None)


class FriendsList(APIView):
    """好友列表"""

    @staticmethod
    def get(request):
        payload = request.user
        user = User.objects.get(id=payload['id'])
        my_friends = Friend.friends(user.id)
        friends_info = {friend.to_dict() for friend in my_friends}
        return render_json({'friends': friends_info})
