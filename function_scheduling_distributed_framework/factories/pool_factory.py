from function_scheduling_distributed_framework.public.utils import import_string
from function_scheduling_distributed_framework.utils import decorators
from function_scheduling_distributed_framework.constant import BrokerEnum, ConcurrentModeEnum


def get_pool(concurrent_mode, concurrent_num, **kwargs):
    concurrent_mode__pool_type_map = {
        ConcurrentModeEnum.THREADING: 'custom_threadpool_executor.CustomThreadPoolExecutor',
        ConcurrentModeEnum.GEVENT: 'custom_gevent_pool_executor.GeventPoolExecutor',
        ConcurrentModeEnum.EVENTLET: 'evenlet_timeout_deco.CustomEventletPoolExecutor',
        ConcurrentModeEnum.ASYNC: 'async_pool_executor.AsyncPoolExecutor',
        ConcurrentModeEnum.SINGLE_THREAD: 'single_thread_executor.SoloExecutor',
    }
    pool_type_str = f'function_scheduling_distributed_framework.concurrent_pool.{concurrent_mode__pool_type_map[concurrent_mode]}'
    pool_type_cls = import_string(pool_type_str)
    return pool_type_cls(concurrent_num, **kwargs)


def get_check_patch_func(concurrent_mode):
    concurrent_mode__check_patch_fun_map = {
        ConcurrentModeEnum.GEVENT: 'custom_gevent_pool_executor.check_gevent_monkey_patch',
        ConcurrentModeEnum.EVENTLET: 'custom_evenlet_pool_executor.check_evenlet_monkey_patch'
    }
    check_patch_fun_str = concurrent_mode__check_patch_fun_map.get(concurrent_mode, 'custom_threadpool_executor.check_not_monkey')
    check_patch_fun_str = f'function_scheduling_distributed_framework.concurrent_pool.{check_patch_fun_str}'
    check_patch_fun = import_string(check_patch_fun_str)
    return check_patch_fun


def get_timeout_deco(concurrent_mode: ConcurrentModeEnum):
    concurrent_mode__timeout_deco_map = {
        ConcurrentModeEnum.THREADING: decorators.timeout,
        ConcurrentModeEnum.SINGLE_THREAD: decorators.timeout,
        ConcurrentModeEnum.GEVENT: 'custom_gevent_pool_executor.gevent_timeout_deco',
        ConcurrentModeEnum.EVENTLET: 'custom_evenlet_pool_executor.evenlet_timeout_deco',
    }
    timeout_deco = concurrent_mode__timeout_deco_map.get(concurrent_mode)
    if timeout_deco:
        if type(timeout_deco) == str:
            timeout_deco_str = f'function_scheduling_distributed_framework.concurrent_pool.{timeout_deco}'
            timeout_deco = import_string(timeout_deco_str)
    return timeout_deco
