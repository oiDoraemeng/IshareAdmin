from flask import Blueprint, render_template, request, session, redirect, url_for

from common.http import fail_api, success_api
from common.loginManagement import LoginManagement
from common.rights import authorize
from common.validate import xss_escape
from model.User import User

loginBP = Blueprint('login', __name__, url_prefix='/login')
loginManagement = LoginManagement()


# 跳转到登录页面
@loginBP.get('/')
def toLogin():
    return render_template('login.html')


# 登录
@loginBP.post('/login')
def login():
    req_json = request.json
    username = xss_escape(req_json.get('username'))
    pwd = xss_escape(req_json.get('pwd'))
    state, info = User().login(username, pwd)
    if state:
        # 登录成功,创建token
        token = User().getId()
        info['token'] = token
        loginManagement.save(token, info)
        return success_api('登陆成功', info)
    else:
        return fail_api(info)


# 退出登录
@loginBP.post('/logout')
@authorize()
def logout():
    token = request.headers.get("token")
    loginManagement.pop(token)
    return success_api('退出登录成功')
