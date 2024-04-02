from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask import request, jsonify, current_app
from functools import wraps
from config import SECRET_KEY

# 生成token, 有效时间为24小时
def generate_token(user_id, expiration=7200):
    serializer = Serializer(SECRET_KEY, expires_in=expiration)
    data = {'user_id': user_id}
    return serializer.dumps(data)


# 解析token
def verify_token(token):
    serializer = Serializer(SECRET_KEY)
    # token正确
    try:
        data = serializer.loads(token)
        return data
    # token过期
    except SignatureExpired:
        return None
    # token错误
    except BadSignature:
        return None
    # token无值
    except Exception as e:
        return None


# 获取登录用户id
def get_user_id():
    token = request.headers.get('Authorization')
    data = verify_token(token)
    user_id = data["user_id"]
    return user_id


def login_required(func):
    """登录校验装饰器
    :param func:函数名
    :return: 闭包函数名
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if verify_token(token):
            return func(*args, **kwargs)
        return jsonify({'code': 401, 'msg': '登录凭证失效,请重新登录!'})

    return decorated
