# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2019/8/8 0008 13:16
import copy
from typing import Callable

from function_scheduling_distributed_framework.constant import BrokerEnum, ConcurrentModeEnum
from function_scheduling_distributed_framework.public.utils import import_string
from function_scheduling_distributed_framework import frame_config


def get_publisher(queue_name, *, log_level_int=10, logger_prefix='', is_add_file_handler=True,
                  clear_queue_within_init=False, is_add_publish_time=True, consuming_function: Callable = None,
                  broker_kind: BrokerEnum = None):
    """
    :param queue_name:
    :param log_level_int:
    :param logger_prefix:
    :param is_add_file_handler:
    :param clear_queue_within_init:
    :param is_add_publish_time:是否添加发布时间，以后废弃，都添加。
    :param consuming_function:消费函数，为了做发布时候的函数入参校验用的，如果不传则不做发布任务的校验，
               例如add 函数接收x，y入参，你推送{"x":1,"z":3}就是不正确的，函数不接受z参数。
    :param broker_kind: 中间件或使用包的种类。
    :return:
    """

    all_kwargs = copy.deepcopy(locals())
    all_kwargs.pop('broker_kind')

    broker_kind__publisher_type_map = {
        BrokerEnum.RABBITMQ_AMQP_STORM: 'rabbitmq_amqpstorm_publisher.RabbitmqPublisherUsingAmqpStorm',
        BrokerEnum.RABBITMQ_RABBIT_PY: 'rabbitmq_rabbitpy_publisher.RabbitmqPublisherUsingRabbitpy',
        BrokerEnum.REDIS_LIST: 'redis_publisher.RedisPublisher',
        BrokerEnum.LOCAL_PYTHON_QUEUE: 'local_python_queue_publisher.LocalPythonQueuePublisher',
        BrokerEnum.RABBITMQ_PIKA: 'rabbitmq_pika_publisher.RabbitmqPublisher',
        BrokerEnum.MONGO_QUEUE: 'mongomq_publisher.MongoMqPublisher',
        BrokerEnum.PERSIST_QUEUE: 'persist_queue_publisher.PersistQueuePublisher',
        BrokerEnum.NSQ: 'nsq_publisher.NsqPublisher',
        BrokerEnum.KAFLA_AUTO_COMMIT: 'kafka_publisher.KafkaPublisher',
        BrokerEnum.REDIS_LIST_AND_SET: 'redis_publisher.RedisPublisher',
        BrokerEnum.SQLACHEMY: 'sqla_queue_publisher.SqlachemyQueuePublisher',
        BrokerEnum.ROCKETMQ: 'rocketmq_publisherRocketmqPublisher',
        BrokerEnum.REDIS_STREAM: 'redis_stream_publisher.RedisStreamPublisher',
        BrokerEnum.ZERO_MQ: 'zeromq_publisher.ZeroMqPublisher',
        BrokerEnum.REDIS_DOUBLE_LIST: 'redis_publisher_lpush.RedisPublisherLpush',
        BrokerEnum.KOMBU: 'kombu_publisher.KombuPublisher',
        BrokerEnum.CONFLUENT_KAFKA: 'confluent_kafka_publisher.ConfluentKafkaPublisher',
        BrokerEnum.MQTT: 'mqtt_publisher.MqttPublisher',
        BrokerEnum.HTTP_SQS: 'httpsqs_publisher.HttpsqsPublisher',
        BrokerEnum.UDP: 'udp_publisher.UDPPublisher',
        BrokerEnum.TCP: 'tcp_publisher.TCPPublisher',
        BrokerEnum.HTTP: 'http_publisher.HTTPPublisher',
    }
    if broker_kind is None:
        broker_kind = frame_config.DEFAULT_BROKER_KIND
    if broker_kind not in broker_kind__publisher_type_map:
        raise ValueError(f'设置的中间件种类数字不正确,你设置的值是 {broker_kind} ')
    publisher_module_str = f'function_scheduling_distributed_framework.publishers.{broker_kind__publisher_type_map[broker_kind]}'
    publisher = import_string(publisher_module_str)
    return publisher(**all_kwargs)
