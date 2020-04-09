import jwt
from django.conf import settings
from jwt import exceptions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication


class JwtQueryParamsAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.query_params.get('token')
        # 1.切割 2.解密第二段、判断是否过期 3.验证第三段合法性
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, True)
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code': 104, 'error': 'token已失效'})
        except jwt.DecodeError:
            raise AuthenticationFailed({'code': 104, 'error': 'toke认证失败'})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'code': 104, 'error': '非法的token'})

        # 三种操作
        # 1.抛出异常，后续不执行
        # 2.return一个元组（1，2），认证通过，在视图中如果调用request.user就是元组的第一个值 auth为2
        # 3. none
        return payload, token
