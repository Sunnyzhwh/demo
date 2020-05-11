
from common import error
from lib.http import render_json


def perm_require(perm_name):
    """权限检查装饰器"""

    def deco(func):
        def wrap(user, sid):
            if user.vip.has_perm(perm_name):
                resp = func(user, sid)
                return resp
            else:
                return render_json(None, error.NOT_HAS_PERM)

        return wrap

    return deco
