# coding=utf8
import redis
from function_scheduling_distributed_framework import frame_config
from function_scheduling_distributed_framework.utils import decorators


class RedisManager(object):
    _pool_dict = {}

    def __init__(self, host='127.0.0.1', port=6379, db=0, password='123456', decode_responses=False):
        pool_key = (host, port, db, password, decode_responses)
        if pool_key not in self.__class__._pool_dict:
            # print ('创建一个连接池')
            self.__class__._pool_dict[pool_key] = redis.ConnectionPool(host=host, port=port, db=db,
                                                                       password=password, decode_responses=decode_responses)
        self._r = redis.Redis(connection_pool=self._pool_dict[pool_key])
        self._ping()

    def get_redis(self):
        """
        :rtype :redis.Redis
        """
        return self._r

    def _ping(self):
        try:
            self._r.ping()
        except Exception as e:
            raise e


# noinspection PyArgumentEqualDefault
class RedisMixin(object):
    """
    可以被作为万能mixin能被继承，也可以单独实例化使用。
    """
    @property
    @decorators.cached_method_result
    def redis_db_filter(self):
        return RedisManager(host=frame_config.REDIS_HOST,
                            port=frame_config.REDIS_PORT,
                            password=frame_config.REDIS_PASSWORD,
                            db=frame_config.REDIS_FILTER_DB).get_redis()

    @property
    @decorators.cached_method_result
    def redis_db_frame(self):
        return RedisManager(host=frame_config.REDIS_HOST,
                            port=frame_config.REDIS_PORT,
                            password=frame_config.REDIS_PASSWORD,
                            db=frame_config.REDIS_MQ_DB).get_redis()

    @property
    @decorators.cached_method_result
    def redis_db_frame_version3(self):
        return RedisManager(host=frame_config.REDIS_HOST,
                            port=frame_config.REDIS_PORT,
                            password=frame_config.REDIS_PASSWORD,
                            db=frame_config.REDIS_MQ_DB,
                            decode_responses=True).get_redis()
