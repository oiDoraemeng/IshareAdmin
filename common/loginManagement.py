
class LoginManagement():
    '''
    登录管理器
    '''
    __instance = None  # 管理器实例
    __loginMap = {}  # 已登录用户的信息

    def __init__(self):
        pass

    # 单例模式,保证全局只有一个登录管理器
    def __new__(cls, *args, **kwargs):
        if LoginManagement.__instance is None:
            LoginManagement.__instance = object.__new__(cls, *args, **kwargs)
        return LoginManagement.__instance

    # 添加一条登录信息
    def save(self, token, data):
        LoginManagement.__loginMap[token] = data

    # 弹出一条登录信息
    def pop(self, token):
        LoginManagement.__loginMap.pop(token)

    # 修改一条登录信息
    def update(self, token, data):
        LoginManagement.__loginMap[token] = data

    # 获取当前用户的登录信息
    def getUser(self, token):
        return LoginManagement.__loginMap.get(token)
