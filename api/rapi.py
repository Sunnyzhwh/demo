from rest_framework.views import APIView
from api.models import User

from api.logic import send_sms, check_vcode, create_token
from common import error
from lib.http import render_json


def get_verify_code(request):
    """获取验证码"""
    # authentication_classes = []
    phone = request.GET.get('phone')
    vcode = send_sms(phone)
    return render_json(vcode)


class Login(APIView):
    """用户登录"""
    authentication_classes = []

    @staticmethod
    def post(request):
        phone = request.data.get('phone')
        vcode = request.data.get('vcode')
        auth_v = check_vcode(phone, vcode)
        # 检查验证码
        if not auth_v:
            return render_json('验证码不正确', error.VCODE_ERROR)
        # 获取用户，或者新注册用户
        user, _ = User.objects.get_or_create(phone=phone)
        payload = {
            'id': user.id,
            'phone': user.phone,
        }
        token = create_token(payload, 30)
        user.token = token
        user.save()
        return render_json(token)


class Profile(APIView):
    # authentication_classes = [JwtQueryParamsAuthentication, ]
    """用户资料"""

    @staticmethod
    def get(request):
        payload = request.user
        # token = request.auth
        user = User.objects.get(id=payload['id'])

        return render_json(user.to_dict)
