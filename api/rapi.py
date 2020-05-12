from django.core.cache import cache
from rest_framework.views import APIView

from api.forms import ProfileForm, UserForm
from api.models import User, Profile

from api.logic import send_sms, check_vcode, create_token, save_upload_file
from common import error
from lib.http import render_json


def get_verify_code(request):
    """获取验证码"""
    # authentication_classes = []
    phone = request.GET.get('phone')
    send_sms(phone)
    # print(vcode)
    return render_json(None)
    # return send_sms(phone)


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


class GetProfile(APIView):
    # authentication_classes = [JwtQueryParamsAuthentication, ]
    """用户资料"""

    @staticmethod
    def get(request):
        payload = request.user
        # token = request.auth
        user = User.objects.get(id=payload['id'])
        key = 'profile-%s' % user.id
        cache_profile = cache.get(key)  # 首先从缓存中获取数据
        print('从缓存中获取：%s' % cache_profile)
        if not cache_profile:
            cache_profile = user.to_dict  # 缓存中没有，从数据库获取
            print('从数据库中获取： %s' % cache_profile)
            cache.set(key, cache_profile)  # 将数据添加到缓存，方便下次获取
            print('添加到缓存')
        return render_json(cache_profile)


class ModifyProfile(APIView):
    """修改个人配置资料"""

    @staticmethod
    def post(request):
        form = ProfileForm(request.POST)
        resp = modify_model(request, form, Profile)
        return resp


class ModifyUser(APIView):
    """修改个人资料"""

    @staticmethod
    def post(request):
        form = UserForm(request.POST)
        resp = modify_model(request, form, User)
        return resp


class UploadAvatar(APIView):
    @staticmethod
    def post(request):
        payload = request.user
        user = User.objects.get(id=payload['id'])
        file = request.FILES.get('avatar')
        if file:
            url = save_upload_file(request, file, user)
            user.avatar = url
            user.save()

            # 修改缓存
            key = 'profile-%s' % user.id
            cache.set(key, user.to_dict)
            return render_json(None)
        else:
            return render_json(None, error.FILE_NOT_FOUND)


def modify_model(request, form, cls):
    """修改表格数据"""
    if form.is_valid():
        payload = request.user
        obj = cls.objects.get(id=payload['id'])
        user = User.objects.get(id=obj.id)
        obj.__dict__.update(form.cleaned_data)
        obj.save()

        # 修改缓存
        key = 'profile-%s' % user.id
        cache.set(key, user.to_dict)
        return render_json(None)
    else:
        return render_json(form.errors, error.PROFILE_ERROR)
