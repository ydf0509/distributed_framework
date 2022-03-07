# from auto_run_on_remote import run_current_script_on_remote
# run_current_script_on_remote()
import json
import os
import time
import random
# from distributed_frame_config import REDIS_HOST
from function_scheduling_distributed_framework import task_deco, BrokerEnum, ConcurrentModeEnum,FunctionResultStatusPersistanceConfig
from function_scheduling_distributed_framework.utils import RedisMixin


# @task_deco('test_queue66', broker_kind=BrokerEnum.RABBITMQ_AMQPSTORM, qps=5, log_level=10, is_print_detail_exception=False, is_show_message_get_from_broker=False,
#            is_using_distributed_frequency_control=True)
@task_deco('test_queue70c',broker_kind=BrokerEnum.REDIS,log_level=20,concurrent_mode=ConcurrentModeEnum.SINGLE_THREAD)
def f(x,y):
    return x+y



if __name__ == '__main__':
    # pass
    # f.clear()
    # for i in range(1000):
    #     f.push(i, i * 2)

    f.consume()
