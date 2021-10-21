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
from function_scheduling_distributed_framework.constant import BrokerEnum


def patch_frame_config(DEFAULT_BROKER_KIND=BrokerEnum.PERSIST_QUEUE,
                       MONGO_CONNECT_URL: str = None,

                       RABBITMQ_USER: str = None,
                       RABBITMQ_PASS: str = None,
                       RABBITMQ_HOST: str = None,
                       RABBITMQ_PORT: int = None,
                       RABBITMQ_VIRTUAL_HOST: str = None,

                       REDIS_HOST: str = None,
                       REDIS_PASSWORD: str = None,
                       REDIS_PORT: int = None,
                       REDIS_DB: int = None,

                       NSQD_TCP_ADDRESSES: list = None,
                       NSQD_HTTP_CLIENT_HOST: str = None,
                       NSQD_HTTP_CLIENT_PORT: int = None,
                       KAFKA_BOOTSTRAP_SERVERS: list = None,

                       SQLACHEMY_ENGINE_URL='sqlite:////sqlachemy_queues/queues.db',
                       **kwargs
                       ):
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

