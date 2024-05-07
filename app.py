# 引入 Flask 和 render_template
from flask import Flask, render_template

# 引入自定义模块
from common.Config import config, ROOT_CONFIG
from common.loginManagement import LoginManagement
from model.User import User
from route import registerRoute


# 创建 Flask 应用程序的函数
def create_app():
    # 初始化模板全局变量
    def init_template_directives(app):
        @app.template_global()
        def authorize(power='common', token=''):
            if token == '':
                return False
            user = LoginManagement().getUser(token)
            if user is None:
                return False
            if user['role'] != 'admin' and power == 'admin':
                return False
            else:
                return True

    # 初始化错误处理页面
    def init_error_views(app):
        @app.errorhandler(403)
        def page_not_found(e):
            return render_template('error/403.html'), 403

        @app.errorhandler(404)
        def page_not_found(e):
            return render_template('error/404.html'), 404

        @app.errorhandler(500)
        def internal_server_error(e):
            return render_template('error/500.html'), 500

    # 初始化超级用户
    def init_admin():
        # 创建超级用户
        dao = User()
        username = ROOT_CONFIG.get('username')
        pwd = ROOT_CONFIG.get('pwd')
        if username is None or pwd is None:
            raise Exception('超级用户账号和信息不能为空')
        data = {
            'id': '0',
            'username': username,
            'realname': '系统根用户',
            'pwd': dao.useMD5(pwd),
            'role': 'admin',
            'enable': '1',
            'token': ''
        }
        dao.deleteByKey('0')
        dao.save(data)

    # 创建 Flask 应用
    app = Flask(__name__)

    # 注册路由
    registerRoute(app)

    # 设置会话密钥
    app.secret_key = 'ZGFiMjlkODY6NTliMz'

    # 加载模板全局变量
    init_template_directives(app)

    # 加载错误处理页面
    init_error_views(app)

    # 创建超级用户
    init_admin()

    print('启动成功')

    return app


# 当直接运行这个脚本时，创建应用并运行
if __name__ == '__main__':
    app = create_app()
    host = config.get('base').get('host')
    port = config.get('base').get('port')
    app.run(host=host, port=port, debug=True)
