import time
from function_scheduling_distributed_framework.set_frame_config import FrameConfig
from function_scheduling_distributed_framework import task_deco, BrokerEnum

#FrameConfig.set_kafka_config(dict(bootstrap_servers=['192.168.2.251:9092']))

@task_deco('test_kafka5', broker_kind=BrokerEnum.KAFLA_AUTO_COMMIT, qps=0.5)
def f(x):
    time.sleep(1)
    print(x)


if __name__ == '__main__':
    # for i in range(100):
    #     f.push(i)
    f.consume()
