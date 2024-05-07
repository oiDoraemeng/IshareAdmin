# -*- coding: utf-8 -*-
# 用户处理模型
# 注意：MongoDB在写入字段时，MDB不会去校验数据字段类型，由我们在程序中进行相应校验；
from model.Base import Base


class User(Base):
    """
    系统用户信息
    """

    def __init__(self):
        super(User, self).__init__('user', 'id')

    # 登录
    def login(self, username, pwd):
        user, count = self.selectByCondition({'username': username})
        if len(user):
            user = user[0]
            if user['enable'] == '0':
                return False, '用户已被禁用'
            elif user['pwd'] != User().useMD5(pwd):
                return False, '密码错误'
            else:
                return True, user
        return False, '用户不存在'


if __name__ == '__main__':
    tmp = User()
    data = {
        'id': tmp.getId(),
        'username': 'test',
        'pwd': 'tesaat',
        'role': 'admddin',
        'enable': '1'
    }
    tmp.updateByKey('0', {'id': '0'})
    # tmp.save(data)
    # tmp.deleteByKey('28ce2eb3e95611ebbdc090769f402963')
    # d = tmp.selectByKey('be44d3a7e95511eb9bb890769f402963')
    # tmp.deleteByCondition({'username':'test'})
    # tmp.updateByKey('67f55d58e95611eb83ad90769f402963',{'pwd':'5201','enable':'0'})
    # ds=tmp.selectByCondition({'username':'test'})
    # ds = tmp.page({'username': 'test'}, 1, 3)
    # d = tmp.login('admin', '1')
    #
    # print(d)
