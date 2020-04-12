import datetime
import random

import jwt
# import requests
from django.conf import settings
from django.core.cache import cache

from tantan import config


# from worker import call_by_worker


def gen_verify_code(length=6):
    return random.randrange(10 ** (length - 1), 10 ** length)


# 将发送验证码任务异步进行
# @call_by_worker
def send_sms(phone):
    vcode = str(gen_verify_code())
    key = 'VerifyCode-%s' % phone
    cache.set(key, vcode, 300)
    # print(cache.get(key))
    sms_config = config.HY_SMS_PARAMS.copy()
    sms_config['msg'] = sms_config['msg'] % vcode
    sms_config['mobile'] = phone
    # response = requests.post(config.HY_SMS_URL, data=sms_config)
    print(vcode)
    return vcode
    # return response


def check_vcode(phone, vcode):
    """检查验证码是否正确"""
    key = 'VerifyCode-%s' % phone
    saved_vcode = cache.get(key)
    # print(vcode)
    # print(saved_vcode)
    return saved_vcode == vcode


def create_token(data, timeout=1):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    salt = settings.SECRET_KEY
    data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=timeout)
    result = jwt.encode(payload=data, key=salt, headers=headers).decode('utf-8')
    return result
