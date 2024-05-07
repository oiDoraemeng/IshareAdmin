from functools import wraps
from flask import abort, request, jsonify, redirect
from common.loginManagement import LoginManagement


# 授权包装器
def authorize(power='common'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 如果是get请求
            token = ''
            if request.method == 'GET':
                # 从参数表拿token
                token = request.args.get('token')
            else:
                # 从请求头拿token
                token = request.headers.get('token')
            if token is None:
                return redirect('/login')

            user = LoginManagement().getUser(token)
            if user == None:
                # 用户已登出
                return redirect('/login')
            else:
                if user['role'] != 'admin' and power == 'admin':
                    if request.method == 'GET':
                        abort(403)
                    else:
                        return jsonify(success=False, msg="权限不足!")

            return func(*args, **kwargs)

        return wrapper

    return decorator
