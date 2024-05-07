import os
import yaml

# 获取yaml文件路径
yamlPath = os.path.join(os.getcwd(), "Config.yaml")

# open方法打开直接读出来
f = open(yamlPath, 'r', encoding='utf-8')
cfg = f.read()
config = yaml.safe_load(cfg)  # 用load方法转字典

# 基础配置
BASE_CONFIG = config.get('base')

# MongoDb配置
MONGODB_CONFIG = config.get('mongodb')

# 日志配置
LOG_CONFIG = config.get('log')

# 系统根用户配置
ROOT_CONFIG = config.get('root')

# 词云配置
WORDS_CONFIG = config.get('wordCloud')

