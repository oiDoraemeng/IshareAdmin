from bson import json_util

# 统一返回json对象
def success_api(msg: str = "成功", data=None):
    """ 成功响应 默认值”成功“ """
    res = {
        'success': True,
        'msg': msg,
        'data': data
    }
    return json_util.dumps(res)


def fail_api(msg: str = "失败", data=None):
    """ 失败响应 默认值“失败” """
    res = {
        'success': False,
        'msg': msg,
        'data': data
    }
    return json_util.dumps(res)


def table_api(msg: str = "", count=0, data=None, limit=10):
    """ 动态表格渲染响应 """
    res = {
        'msg': msg,
        'code': 0,
        'data': data,
        'count': count,
        'limit': limit
    }
    return json_util.dumps(res)
