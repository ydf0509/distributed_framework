# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2019/8/8 0008 13:19
import copy
from function_scheduling_distributed_framework.constant import BrokerEnum, ConcurrentModeEnum
from function_scheduling_distributed_framework.public.utils import import_string
from function_scheduling_distributed_framework import frame_config


def get_consumer(*args, broker_kind: BrokerEnum = None, **kwargs):
    """
    :param args: 入参是AbstractConsumer的入参
    :param broker_kind:
    :param kwargs:
    :return:
    """

    broker_kind__consumer_type_map = {
        BrokerEnum.RABBITMQ_AMQP_STORM: 'rabbitmq_amqpstorm_consumer.RabbitmqConsumerAmqpStorm',
        BrokerEnum.RABBITMQ_RABBIT_PY: 'rabbitmq_rabbitpy_consumer.RabbitmqConsumerRabbitpy',
        BrokerEnum.REDIS_LIST: 'redis_consumer.RedisConsumer',
        BrokerEnum.LOCAL_PYTHON_QUEUE: 'local_python_queue_consumer.LocalPythonQueueConsumer',
        BrokerEnum.RABBITMQ_PIKA: 'rabbitmq_pika_consumer.RabbitmqConsumer',
        BrokerEnum.MONGO_QUEUE: 'mongomq_consumer.MongoMqConsumer',
        BrokerEnum.PERSIST_QUEUE: 'persist_queue_consumer.PersistQueueConsumer',
        BrokerEnum.NSQ: 'nsq_consumer.NsqConsumer',
        BrokerEnum.KAFLA_AUTO_COMMIT: 'kafka_consumer.KafkaConsumer',
        BrokerEnum.REDIS_LIST_AND_SET: 'redis_consumer_ack_able.RedisConsumerAckAble',
        BrokerEnum.SQLACHEMY: 'sqlachemy_consumer.SqlachemyConsumer',
        BrokerEnum.ROCKETMQ: 'rocketmq_consumer.RocketmqConsumer',
        BrokerEnum.REDIS_STREAM: 'redis_stream_consumer.RedisStreamConsumer',
        BrokerEnum.ZERO_MQ: 'zeromq_consumer.ZeroMqConsumer',
        BrokerEnum.REDIS_DOUBLE_LIST: 'redis_brpoplpush_consumer.RedisBrpopLpushConsumer',
        BrokerEnum.KOMBU: 'kombu_consumer.KombuConsumer',
        BrokerEnum.CONFLUENT_KAFKA: 'kafka_consumer_manually_commit.KafkaConsumerManuallyCommit',
        BrokerEnum.MQTT: 'mqtt_consumer.MqttConsumer',
        BrokerEnum.HTTP_SQS: 'httpsqs_consumer.HttpsqsConsumer',
        BrokerEnum.UDP: 'udp_consumer.UDPConsumer',
        BrokerEnum.TCP: 'tcp_consumer.TCPConsumer',
        BrokerEnum.HTTP: 'http_consumer.HTTPConsumer',
    }
    if broker_kind is None:
        broker_kind = frame_config.DEFAULT_BROKER_KIND
    if broker_kind not in broker_kind__consumer_type_map:
        raise ValueError(f'设置的中间件种类数字不正确,你设置的值是 {broker_kind} ')
    consumer_module_str = f'function_scheduling_distributed_framework.consumers.{broker_kind__consumer_type_map[broker_kind]}'
    consumer = import_string(consumer_module_str)
    return consumer(*args, **kwargs)
