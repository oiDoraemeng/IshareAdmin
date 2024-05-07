from route.index import indexBP
from route.login import loginBP
from route.user import userBP



def registerRoute(app):
    '''
    注册所有蓝图
    :param app:
    :return:
    '''
    app.register_blueprint(indexBP)
    app.register_blueprint(loginBP)
    app.register_blueprint(userBP)
