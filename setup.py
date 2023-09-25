# coding=utf-8

from setuptools import setup, find_packages

# with open("README.md", "r",encoding='utf8') as fh:
#     long_description = fh.read()
print(find_packages())
setup(
    name='function_scheduling_distributed_framework',  #
    version='12.9',
    description=(
        'function scheduling distributed framework,support threading,gevent,eventlet,asyncio concurrent,support all kinds of message queue,and has manay control way'
    ),
    # long_description=open('README.md', 'r',encoding='utf8').read(),
    keywords=["distributed-framework", "function-scheduling", "rabbitmq", "rocketmq", "kafka", "nsq", "redis", "disk",
              "sqlachemy", "consume-confirm", "timing", "task-scheduling", "apscheduler", "pulsar", "mqtt", "kombu"],
    long_description_content_type="text/markdown",
    long_description=open('README.md', 'r', encoding='utf8').read(),
    author='bfzs',
    author_email='ydf0509@sohu.com',
    maintainer='ydf',
    maintainer_email='ydf0509@sohu.com',
    license='BSD License',
    # packages=['douban'], #
    packages=find_packages(),
    # packages=['function_scheduling_distributed_framework'], # 这样内层级文件夹的没有打包进去。
    include_package_data=True,
    platforms=["all"],
    url='https://github.com/ydf0509/distributed_framework',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'eventlet==0.31.0',
        'gevent==23.9.1',
        'pymongo==3.5.1',
        'AMQPStorm==2.7.1',
        'rabbitpy==2.0.1',
        'decorator==4.4.0',
        # 'pysnooper==0.0.11',
        'Flask',
        'flask_bootstrap',
        'flask_wtf',
        'wtforms',
        'flask_login',
        'tomorrow3==1.1.0',
        'persist-queue>=0.4.2',
        'elasticsearch',
        'kafka-python==1.4.6',
        'requests',
        'gnsq==1.0.1',
        'psutil',
        'sqlalchemy==1.3.10',
        'sqlalchemy_utils==0.36.1',
        'apscheduler==3.7.0',
        'pikav0',
        'pikav1',
        'redis2',
        'redis3',
        'redis',
        'nb_log>=6.4',
        'rocketmq',
        'zmq',
        'pyzmq',
        'kombu',  # 'kombu==4.6.11',
        # 'confluent_kafka==1.7.0',
        'paho-mqtt',
        'setuptools_rust',
        'fabric2==2.6.0',  # 有的机器包rust错误， 这样做 curl https://sh.rustup.rs -sSf | sh
        'nats-python',
        'nb_filelock',
        'aiohttp',
        'pysnooper',
    ]
)
"""
官方 https://pypi.org/simple
清华 https://pypi.tuna.tsinghua.edu.cn/simple
豆瓣 https://pypi.douban.com/simple/ 
阿里云 https://mirrors.aliyun.com/pypi/simple/
腾讯云  http://mirrors.tencentyun.com/pypi/simple/

打包上传
python setup.py sdist upload -r pypi

# python setup.py bdist_wheel
python setup.py bdist_wheel ; python -m twine upload dist/function_scheduling_distributed_framework-12.9-py3-none-any.whl
python setup.py sdist & twine upload dist/function_scheduling_distributed_framework-10.9.tar.gz

最快的下载方式，上传立即可安装。阿里云源同步官网pypi间隔要等很久。
./pip install function_scheduling_distributed_framework==3.5 -i https://pypi.org/simple   
最新版下载
./pip install function_scheduling_distributed_framework --upgrade -i https://pypi.org/simple       
"""
