import re

from flask import Blueprint, render_template, request, session

from common.http import table_api, fail_api, success_api
from common.loginManagement import LoginManagement
from common.rights import authorize
from common.validate import xss_escape, regConvert
from model.User import User

userBP = Blueprint('user', __name__, url_prefix='/user')
dao = User()  # 持久层对象
loginManagement = LoginManagement()


# 跳转到用户增加
@userBP.get('/add')
@authorize()
def add():
    return render_template('user/add.html')


@userBP.post('/save')
@authorize()
def save():
    req_json = request.json
    username = xss_escape(req_json.get('username'))
    pwd = xss_escape(req_json.get('pwd'))
    role = 'common'
    enable = '1'
    data = {
        'id': dao.getId(),
        'username': username,
        'realname': username,
        'pwd': dao.useMD5(pwd),
        'role': role,
        'enable': enable,
        'token': ''
    }
    if dao.selectByCondition({'username': username})[1] > 0:
        return fail_api('账号已存在')
    if dao.save(data):
        return success_api(msg="添加成功")
    else:
        return fail_api(msg='添加失败')


# 删除用户
@userBP.delete('/remove/<id>')
@authorize('admin')
def delete(id):
    if id == '0':
        return fail_api('系统根用户不允许任何修改')
    if dao.deleteByKey(id):
        return success_api(msg="删除成功")
    else:
        return fail_api(msg='删除失败')


#  跳转到编辑用户
@userBP.get('/edit/<id>')
@authorize('admin')
def edit(id):
    data = dao.selectByKey(id)
    return render_template('user/edit.html', data=data)


#  编辑用户
@userBP.put('/update')
@authorize('admin')
def update():
    req_json = request.json
    id = xss_escape(req_json.get('id'))
    if id == '0':
        return fail_api('系统根用户不允许任何修改')
    username = xss_escape(req_json.get('username'))
    role = xss_escape(req_json.get('role'))
    pwd = xss_escape(req_json.get('pwd'))

    user = dao.selectByKey(id)
    # 判断用户是否已被删除
    if user is None:
        return fail_api('操作失败,该用户不存在或已被删除')

    if user['pwd'] != pwd:
        pwd = dao.useMD5(pwd)
    enable = xss_escape(req_json.get('enable'))

    if dao.selectByCondition({'username': username})[1] > 0:
        if not dao.selectByKey(id)['username'] == username:
            return fail_api('账号已存在')

    data = {
        'username': username,
        'realname': username,
        'pwd': pwd,
        'role': role,
        'enable': enable
    }
    if dao.updateByKey(id, data):
        return success_api(msg="更新成功")
    else:
        return fail_api('未作任何变动')


# 启用用户
@userBP.put('/enable')
@authorize('admin')
def enable():
    req_json = request.json
    id = xss_escape(req_json.get('id'))
    if id == '0':
        return fail_api('系统根用户不允许任何修改')
    if dao.updateByKey(id, {'enable': '1'}):
        return success_api(msg="启用成功")
    else:
        return fail_api('启用失败')


# 禁用用户
@userBP.put('/disable')
@authorize('admin')
def dis_enable():
    req_json = request.json
    id = xss_escape(req_json.get('id'))
    if id == '0':
        return fail_api('系统根用户不允许任何修改')
    if dao.updateByKey(id, {'enable': '0'}):
        return success_api(msg="禁用成功")
    else:
        return fail_api('禁用失败')


# 批量删除
@userBP.delete('/batchRemove')
@authorize('admin')
def batch_remove():
    ids = request.form.getlist('ids[]')
    flag = False
    if '0' in ids:
        ids.remove('0')
        flag = True

    if dao.batchRemove(ids):
        if flag:
            return success_api(msg="批量删除成功,但根用户不允许删除")
        else:
            return success_api(msg="批量删除成功")
    else:
        return fail_api('批量删除失败')
