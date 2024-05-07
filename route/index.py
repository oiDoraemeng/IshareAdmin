from flask import Blueprint, render_template, request

from common.loginManagement import LoginManagement
from common.rights import authorize
from model.User import User
from model.models import Notice, CovidData

indexBP = Blueprint('index', __name__, url_prefix='/')
userDao = User()


# 首页
@indexBP.get('')
@authorize()
def index():
    token = request.args.get('token')
    user = LoginManagement().getUser(token)
    userList = userDao.selectByCondition({})[0]
    return render_template('index.html', user=user, userList=userList, token=token)
