import time

from test_frame.test_broker.test_consume import f

f.clear()
for i in range(1,1000000):
    # time.sleep(0.2)
    if i == 0:
        print(time.strftime("%H:%M:%S"), '发布第一条')
    if i % 10000 == 0:
        print(time.strftime("%H:%M:%S"), f'发布第{i}条')
    f.push(i, i * 2)

if __name__ == '__main__':
    pass
    # f.multi_process_pub_params_list([{'a':i,'b':2*i} for i in range(100000)],process_num=5)