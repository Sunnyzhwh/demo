import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
# Create your views here.


class Login(APIView):
    """用户登录"""

    def post(self, request, *args, **kwargs):
        nickname = request.data.get('nickname')
        pwd = request.data.get('pwd')

        user = models.User.objects.filter(nickname=nickname, pwd=pwd).first()
        if not user:
            return Response({'code': 101, 'error': '用户名或密码错误'})

        random_string = str(uuid.uuid4())
        user.token = random_string
        user.save()
        return Response({'code': 100, 'data': random_string})
