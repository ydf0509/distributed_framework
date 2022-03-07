import asyncio

import aiohttp
import aiomysql

from function_scheduling_distributed_framework import task_deco,ConcurrentModeEnum,BrokerEnum

aiomysql.connect()

'''
演示 specify_async_loop 用法，根据自己代码需要按情况使用specify_async_loop
这里举得是aiohttp例子，例如还有aiomysql例子，aioredis例子
'''


loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)

# 如果使用全局变量session，必须指定loop，并且这个loop同时传给ClientSession类和task_deco装饰器，否则报错。
@task_deco('test_specify_loop',concurrent_mode=ConcurrentModeEnum.ASYNC,specify_async_loop=loop)
async def f(url):
    async with session.get(url) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])

# 如果没使用全局变量session，task_deco装饰器无需指定specify_async_loop入参
@task_deco('test_specify_loop',concurrent_mode=ConcurrentModeEnum.ASYNC)
async def f2(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

if __name__ == '__main__':
    for p in range(1,100):
        urlx = f'https://www.cnblogs.com/#p{p}'
        f.push(urlx)
        f2.push(urlx)
    f.consume()
    f2.consume()