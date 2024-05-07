# -*- coding: utf-8 -*-
# 公共基础模型、数据库表
import copy
import uuid
import hashlib

from bson import ObjectId

from common.Config import LOG_CONFIG, MONGODB_CONFIG
from common.LogUtil import Logger
from common.MongoDbUtil import MongoDbUtil

logger = Logger(LOG_CONFIG)


class Base:
    def __init__(self, collection, primaryKey):
        self.collection = collection  # 数据库集合名
        self.primaryKey = primaryKey  # 当前集合的主键字段
        self.conn = None  # 数据库连接
        self._getConn()

    def _getConn(self):
        """
        # 获取MongoDB数据库连接
        :return: 数据库连接
        """
        if self.conn is None:
            try:
                self.conn = MongoDbUtil(MONGODB_CONFIG)
            except Exception as e:
                logger.error('实例化MongoDbs失败,{}'.format(e))

    def save(self, data):
        """
        向集合中添加一条数据
        :param data:待添加的数据
        :return:添加的_id值
        """
        try:
            _id = self.conn.insert_one(self.collection, data)
            return _id
        except Exception as e:
            logger.error("插入单条数据失败,{}".format(e))
            return None

    def saveMany(self, data):
        """
        向集合中添加一条数据
        :param data:待添加的数据
        :return:添加成功的数量
        """
        try:
            ret = self.conn.insert_many(self.collection, data)
            return ret
        except Exception as e:
            logger.error("插入多条数据失败{}".format(e))
            return -1

    def deleteByKey(self, key):
        """
        根据默认主键删除数据
        :param key: 要删除数据的主键的值
        :return:删除的条数
        """
        try:
            ret = self.conn.delete(self.collection, {self.primaryKey: key})
            return ret
        except Exception as e:
            logger.error("根据主键删除数据失败{}".format(e))
            return -1

    def batchRemove(self, keys):
        """
        根据主键批量删除
        :param keys:主键列表
        :return:删除的条数
        """
        try:
            ret = self.conn.delete(self.collection, {self.primaryKey: {'$in': keys}})
            return ret
        except Exception as e:
            logger.error("批量删除数据失败,{}".format(e))
            return -1

    def deleteByCondition(self, condition):
        """
        根据条件删除数据
        :param condition: 条件
        :return: 成功删除的的条数
        """
        try:
            ret = self.conn.delete(self.collection, condition)
            return ret
        except Exception as e:
            logger.error("根据条件删除数据失败,{}".format(e))
            return -1

    def updateByKey(self, key, data):
        """
        根据默认主键更新数据
        :param key: 主键的值
        :param data: 数据
        :return:更新的数量
        """
        try:
            state = self.conn.update_one(self.collection, {self.primaryKey: key}, data)
            return state
        except Exception as e:
            logger.error("根据主键更新数据失败{}".format(e))
            return -1

    def updateByCondition(self, condition, data):
        """
        根据条件更新数据
        :param condition:查询条件
        :param data:更新数据
        :return:更新的状态,bool
        """
        try:
            state = self.conn.update_batch(self.collection, condition, data)
            return state
        except Exception as e:
            logger.error("批量更新数据失败{}".format(e))
            return -1

    def selectByKey(self, key, column=None):
        """
        根据默认主键获取数据
        :param column:
        :param key:主键的值
        :return:查询到的数据,默认为None
        """
        data = self.conn.find_one(self.collection, {self.primaryKey: key}, column)
        return data

    def selectByCondition(self, condition, column=None):
        """
        根据条件获取数据
        :param column:
        :param condition: 条件
        :return: 数据,数据条数
        """

        data = list(self.conn.find(self.collection, condition, column))
        count = len(data)
        return data, count

    def page(self, condition, page=1, limit=10):
        """
        分页查询
        :param condition:查询条件
        :param page:当前页数
        :param limit:每页数据条数
        :return:数据,数据总数
        """

        total_num = self.conn.counts(self.collection, condition)
        page_total_num = total_num // limit  # 总页数
        if total_num % limit: page_total_num += 1
        # 范围限制
        if page < 1:
            page = 1
        if page_total_num == 0:
            start = 0
        elif page > page_total_num:
            start = (page_total_num - 1) * limit
        else:
            start = (page - 1) * limit
        data = list(self.conn.find(self.collection, condition).limit(limit).skip(start))

        return data, total_num

    def aggregate(self, condition):
        """
        多表查询
        :param condition:查询条件
        :param page:当前页数
        :param limit:每页数据条数
        :return:数据,数据总数
        """

        data = list(self.conn.aggregate(self.collection, condition))
        return data, len(data)

    def lookup(self, From, localField, foreignField, As):
        """
        集算器连表
        :param From:从表表名
        :param localField:主表字段
        :param foreignField:从表外键字段
        :param As:别名
        :return:
        """
        data = {
            '$lookup':
                {
                    'from': From,
                    'localField': localField,
                    'foreignField': foreignField,
                    'as': As
                }
        }
        return data

    def match(self, condition):
        """
        集算器筛选条件
        :param condition:匹配条件
        :return:
        """
        data = {
            '$match': condition
        }
        return data

    def sort(self, condition):
        """
        集算器筛选条件
        :param condition:匹配条件
        :return:
        """
        data = {
            '$sort': condition
        }
        return data

    def aggregatePage(self, condition, page=1, limit=10):
        """
        多表分页查询
        :param condition:查询条件
        :param page:当前页数
        :param limit:每页数据条数
        :return:数据,数据总数
        """

        total_num = self.conn.aggregate_counts(self.collection, copy.deepcopy(condition))
        page_total_num = total_num // limit  # 总页数
        if total_num % limit: page_total_num += 1
        # 范围限制
        if page < 1:
            page = 1
        if page_total_num == 0:
            start = 0
        elif page > page_total_num:
            start = (page_total_num - 1) * limit
        else:
            start = (page - 1) * limit

        condition.append({'$skip': start})
        condition.append({'$limit': limit})
        data = list(self.conn.aggregate(self.collection, condition))

        return data, total_num

    def useMD5(self, text):
        md5 = hashlib.md5()
        md5.update(text.encode(encoding='utf-8'))
        return md5.hexdigest()

    def getId(self):
        return uuid.uuid4().hex

    def getObjectId(self):
        return ObjectId()
