# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2020/4/11 0011 0:56
"""

使用覆盖的方式，做配置。
"""
import copy
import re
from nb_log import nb_print, stderr_write, stdout_write
from nb_log.monkey_print import is_main_process, only_print_on_main_process
from function_scheduling_distributed_framework import frame_config
import typing
from function_scheduling_distributed_framework.constant import BrokerEnum

if typing.TYPE_CHECKING:
    from typing import TypedDict


    class RedisConfigDict(TypedDict):
        host: str
        port: int
        password: str
        db: int


    class MongoConfigDict(TypedDict):
        host: typing.Union[str, typing.List[str]]
        username: str
        password: str
        db: str


    class RabbitmqConfigDict(TypedDict):
        host: str
        port: int
        user: str
        passwd: str
        vhost: str


    class KafkaConfigDict(TypedDict):
        bootstrap_servers: typing.List[str]


class FrameConfig:
    @staticmethod
    def set_base_config(self, **kwargs):
        for k, v in kwargs.items():
            setattr(frame_config, k, v)

    @staticmethod
    def set_mongo_config(self, mongo_config: 'MongoConfigDict', default_broker=True):
        host = mongo_config["host"]
        if type(host) is list:
            host = ','.join(mongo_config["host"])
        mongo_connect_url = f'mongodb://{mongo_config["username"]}:{mongo_config["password"]}@{host}/{mongo_config["db"]}'
        frame_config.MONGO_CONNECT_URL = mongo_connect_url
        if default_broker:
            frame_config.DEFAULT_BROKER_KIND = BrokerEnum.MONGOMQ

    @staticmethod
    def set_redis_config(redis_config: 'RedisConfigDict', default_broker=True):
        frame_config.REDIS_MQ_DB = redis_config['db']
        frame_config.REDIS_HOST = redis_config['host']
        frame_config.REDIS_PORT = redis_config['port']
        frame_config.REDIS_PASSWORD = redis_config['password']
        if default_broker:
            frame_config.DEFAULT_BROKER_KIND = BrokerEnum.REDIS_STREAM

    @staticmethod
    def set_kafka_config(kafka_config: 'KafkaConfigDict', default_broker=True):
        frame_config.KAFKA_BOOTSTRAP_SERVERS = kafka_config['bootstrap_servers']
        if default_broker:
            frame_config.DEFAULT_BROKER_KIND = BrokerEnum.KAFKA

    @staticmethod
    def set_rabbitmq_config(self, rabbitmq_config: 'RabbitmqConfigDict', default_broker=True):
        frame_config.RABBITMQ_HOST = rabbitmq_config['host']
        frame_config.RABBITMQ_PORT = rabbitmq_config['port']
        frame_config.RABBITMQ_USER = rabbitmq_config['user']
        frame_config.RABBITMQ_PASS = rabbitmq_config['passwd']
        frame_config.RABBITMQ_VIRTUAL_HOST = rabbitmq_config['vhost']
        if default_broker:
            frame_config.DEFAULT_BROKER_KIND = BrokerEnum.RABBITMQ_AMQPSTORM


# noinspection PyPep8Naming
# 这是手动调用函数设置配置，框架会自动调用use_config_form_distributed_frame_config_module读当前取项目根目录下的distributed_frame_config.py，不需要嗲用这里
def patch_frame_config(MONGO_CONNECT_URL: str = None,

                       RABBITMQ_USER: str = None,
                       RABBITMQ_PASS: str = None,
                       RABBITMQ_HOST: str = None,
                       RABBITMQ_PORT: int = None,
                       RABBITMQ_VIRTUAL_HOST: str = None,

                       REDIS_HOST: str = None,
                       REDIS_PASSWORD: str = None,
                       REDIS_PORT: int = None,
                       REDIS_MQ_DB: int = None,

                       NSQD_TCP_ADDRESSES: list = None,
                       NSQD_HTTP_CLIENT_HOST: str = None,
                       NSQD_HTTP_CLIENT_PORT: int = None,
                       KAFKA_BOOTSTRAP_SERVERS: list = None,

                       SQLACHEMY_ENGINE_URL='sqlite:////sqlachemy_queues/queues.db'

                       ):
    """
    对框架的配置使用猴子补丁的方式进行更改。利用了模块天然是单利的特性。格式参考frame_config.py
    :return:
    """
    kw = copy.copy(locals())
    for var_name, var_value in kw.items():
        if var_value is not None:
            setattr(frame_config, var_name, var_value)
    nb_print('使用patch_frame_config 函数设置框架配置了。')
    show_frame_config()


def show_frame_config():
    only_print_on_main_process('显示当前的项目中间件配置参数')
    for var_name in dir(frame_config):
        if var_name.isupper():
            var_value = getattr(frame_config, var_name)
            if var_name == 'MONGO_CONNECT_URL':
                if re.match('mongodb://.*?:.*?@.*?/.*', var_value):
                    mongo_pass = re.search('mongodb://.*?:(.*?)@', var_value).group(1)
                    mongo_pass_encryption = f'{"*" * (len(mongo_pass) - 2)}{mongo_pass[-1]}' if len(
                        mongo_pass) > 3 else mongo_pass
                    var_value_encryption = re.sub(r':(\w+)@', f':{mongo_pass_encryption}@', var_value)
                    only_print_on_main_process(f'{var_name}:             {var_value_encryption}')
                    continue
            if 'PASS' in var_name and var_value is not None and len(var_value) > 3:  # 对密码打*
                only_print_on_main_process(f'{var_name}:                {var_value[0]}{"*" * (len(var_value) - 2)}{var_value[-1]}')
            else:
                only_print_on_main_process(f'{var_name}:                {var_value}')

