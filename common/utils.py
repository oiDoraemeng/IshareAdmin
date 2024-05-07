import datetime
import hashlib
import random
import socket
import time
import uuid

"""
常用函数库
"""


def calculate_file_md5(filepath):
    """
    计算文件的md5值
    :param filepath:文件的路径
    :return:文件的md5值
    """
    try:
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            while True:
                # 分片计算,防止文件过大造成内存不足
                temp = f.read(8192)
                if temp == b"":
                    break
                md5.update(temp)
        return md5.hexdigest()
    except Exception as e:
        raise Exception('计算md5失败,{}'.format(e))


def get_host_ip():
    """
    获取服务器的ip地址
    :return: string 服务器ip地址
    """
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip


def get_host_name():
    """
    获取服务器名
    :return:
    """
    return socket.gethostname()


def get_mac_address():
    """
    获取服务器MAC地址
    :return:
    """
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def get_md5(string):
    """
    获取字符串的md5值
    :param string:
    :return:字符串的md5
    """
    hl = hashlib.md5()
    hl.update(string.encode(encoding='utf-8'))
    return hl.hexdigest()


def get_current_time(format_str='%Y-%m-%d %H:%M:%S'):
    """
    获取当前时间
    :param format_str: 格式字符串,默认%Y-%m-%d %H:%M:%S
    :return:str 当前时间
    """
    return datetime.datetime.now().strftime(format_str)


def get_time_stamp():
    """
    获取当前时间的时间戳
    :return: 13位时间戳
    """
    return int(round(time.time() * 1000))


def get_random_str(length=10):
    """
    获取指定长度的由大小写字母、数字组成的随机字符串
    :param length:id的长度
    :return: str 一个指定长度的字符串
    """
    str_list = []
    base_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
    max_index = len(base_str) - 1
    for i in range(length):
        str_list.append(base_str[random.randint(0, max_index)])
    return "".join(str_list)


def blob_to_base64():
    """
    二进制对象转base64编码
    :return:str base64编码
    """
    pass


def base64_to_blob(base64):
    """
    base64编码转二进制对象
    :return:blob 二进制对象
    """
    pass
